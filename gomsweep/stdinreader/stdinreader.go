package stdinreader

import (
	"fmt"
	"io"
	"os"
	"syscall"
	"time"

	"github.com/pkg/term/termios"
)

///*
// Term represents an asynchronous communications port.
type Term struct {
	Name string
	Fd   int
	Orig syscall.Termios // original state of the terminal, see Open and Restore
}

// Open opens an asynchronous communications port.
func Open(name string, options ...func(*Term) error) (*Term, error) {
	fd, e := syscall.Open(name, syscall.O_NOCTTY|syscall.O_CLOEXEC|syscall.O_NDELAY|syscall.O_RDWR, 0666)
	if e != nil {
		return nil, &os.PathError{"open", name, e}
	}

	t := Term{Name: name, Fd: fd}
	if err := termios.Tcgetattr(uintptr(t.Fd), &t.Orig); err != nil {
		time.Sleep(time.Second * 100)
		return nil, err
	}
	if err := t.SetOption(options...); err != nil {
		return nil, err
	}
	return &t, syscall.SetNonblock(t.Fd, false)
}

// Restore restores the state of the terminal captured at the point that
// the terminal was originally opened.
func (t *Term) Restore() error {
	return termios.Tcsetattr(uintptr(t.Fd), termios.TCIOFLUSH, &t.Orig)
}

// Read reads up to len(b) bytes from the terminal. It returns the number of
// bytes read and an error, if any. EOF is signaled by a zero count with
// err set to io.EOF.
func (t *Term) Read(b []byte) (int, error) {
	n, e := syscall.Read(t.Fd, b)
	if n < 0 {
		n = 0
	}
	if n == 0 && len(b) > 0 && e == nil {
		return 0, io.EOF
	}
	if e != nil {
		return n, &os.PathError{"read", t.Name, e}
	}
	return n, nil
}

// SetOption takes one or more option function and applies them in order to Term.
func (t *Term) SetOption(options ...func(*Term) error) error {
	for _, opt := range options {
		if err := opt(t); err != nil {
			return err
		}
	}
	return nil
}

// RawMode places the terminal into raw mode.
func RawMode(t *Term) error {
	var a syscall.Termios
	if err := termios.Tcgetattr(uintptr(t.Fd), (*syscall.Termios)(&a)); err != nil {
		return err
	}
	termios.Cfmakeraw((*syscall.Termios)(&a))
	a.Oflag |= syscall.OPOST
	return termios.Tcsetattr(uintptr(t.Fd), termios.TCSANOW, (*syscall.Termios)(&a))
}

//*/

//func EnableOutputPostprocess(a *syscall.Termios) uintptr {
//a.Oflag |= syscall.OPOST
//return termios.TCSANOW
//}

func init() {
	t, _ = Open("/dev/tty")
	t.SetOption(RawMode)
}

type Inpt struct {
	B      []byte
	Moment time.Time
}

var t *Term

func pullLoop(depo chan Inpt) {
	for {
		buf := make([]byte, 1)
		length, err := t.Read(buf)
		fmt.Printf("Read something: %v\n", buf)
		if length != 1 {
			panic(fmt.Sprintf("Read more than 1 bytes, '%v'", length))
		}
		if err != nil {
			panic(err)
		}
		i := Inpt{
			B:      make([]byte, len(buf)),
			Moment: time.Now(),
		}
		copy(i.B, buf)
		depo <- i
	}
}

func NewKeyGetter() chan Inpt {
	rv := make(chan Inpt)
	go pullLoop(rv)
	return rv
}

func Restore() {
	fmt.Printf("Restoring our terminal!\n")
	err := t.Restore()
	if err != nil {
		fmt.Printf("Error on restore: %v\n", err)
	}
}

func TimeFilter(keys chan Inpt) chan Inpt {
	rv := make(chan Inpt)
	go func() {
		for {
			k := <-keys
			for {
				time.Sleep(3 * time.Millisecond)
				shouldexit := false
				select {
				case another := <-keys:
					k.B = append(k.B, another.B...)
					k.Moment = another.Moment
				default:
					shouldexit = true
				}
				if shouldexit {
					break
				}
			}
			rv <- k
		}
	}()
	return rv
}
