package main

import (
	"fmt"

	"github.com/lelandbatey/minesweeper/gomsweep/stdinreader"
)

func main() {
	fmt.Println("Minesweeper!")
	defer stdinreader.Restore()
	keys := stdinreader.TimeFilter(stdinreader.NewKeyGetter())
	for {
		fmt.Printf("waiting to get from channel...\n")
		k := <-keys
		fmt.Printf("bytes: %v, time: %v\n", k.B, k.Moment)
		if k.B[0] == 3 {
			fmt.Printf("Recieved CTRL-C, exiting\n")
			return
		}
	}
}
