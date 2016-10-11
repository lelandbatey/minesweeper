package gomsweep

import "fmt"

type Contents int

const (
	Mine Contents = iota
	Flag
	Smiley
	Empty
)

type Direction int

const (
	Up Direction = iota
	Down
	Left
	Right
)

type Minefield struct {
	Height    int
	Width     int
	Minecount int
	Brandnew  bool
	Grid      [][]*Cell
}

type Cell struct {
	X            int
	Y            int
	Minecontacts int
	Contents     Contents
	Probed       bool
	Flaged       bool
	Transparent  bool
	Selected     bool
	Field        *Minefield
}

func NewMinefield(height int, width int, mines int) *Minefield {
	rv := &Minefield{
		Height:    height,
		Width:     width,
		Minecount: mines,
		Brandnew:  true,
	}
	rows := make([][]*Cell, 0)
	for h := 0; h < height; h++ {
		col := make([]*Cell, 0)

		for w := 0; w < width; w++ {
			c := NewCell(w, h, rv)
			col = append(col, c)
		}

		rows = append(rows, col)
	}
	rv.Grid = rows
	rv.Grid[0][0].Selected = true
	rv.populateBombs()

	return rv
}

func NewCell(x int, y int, field *Minefield) *Cell {
	rv := &Cell{
		X:            x,
		Y:            y,
		Field:        field,
		Minecontacts: 0,
		Contents:     Empty,
	}
	return rv
}

func (m *Minefield) Selected() *Cell {
	for h := 0; h < m.Height; h++ {
		for w := 0; w < m.Width; w++ {
			c := m.Grid[w][h]
			if c.Selected {
				return c
			}
		}
	}
	return nil
}

func (m *Minefield) populateBombs() {
	if m.Minecount == 0 {
		m.Minecount = int(0.15 * float64(m.Height*m.Width))
	}
}

func (m *Minefield) MoveSelected(d Direction) {
	deltmap := map[Direction][]int{
		Up:    {0, -1},
		Down:  {0, 1},
		Left:  {-1, 0},
		Right: {1, 0},
	}

	delt := deltmap[d]
	c := m.Selected()

	x, y := c.X+delt[0], c.Y+delt[1]
	if x >= c.Field.Width || x < 0 {
		return
	}
	if y >= c.Field.Height || y < 0 {
		return
	}
	newsel := m.Grid[x][y]
	c.Selected = false
	newsel.Selected = true
}

// Probe probes a cell for a mine, returning false if there's no
// mine, or true if a probed cell contains a mine.
func (c *Cell) Probe() bool {
	if c.Flaged {
		return false
	}
	if !c.Probed {
		c.Probed = true
		if c.Contents == Mine {
			return true
		}
		if c.Minecontacts == 0 {
			adjacent := c.Adjacent()
			for _, adj := range adjacent {
				lose_game := adj.Probe()
				if lose_game {
					return lose_game
				}
			}
		}
	}
	return false
}

func (c *Cell) Adjacent() []*Cell {
	deltas := [][]int{
		{-1, -1},
		{-1, 0},
		{-1, 1},
		{0, -1},
		{0, 1},
		{1, -1},
		{1, 0},
		{1, 1},
	}
	rv := []*Cell{}
	for _, delt := range deltas {
		x, y := c.X+delt[0], c.Y+delt[1]
		if x >= c.Field.Width || x < 0 {
			continue
		}
		if y >= c.Field.Height || y < 0 {
			continue
		}
		rv = append(rv, c.Field.Grid[x][y])
	}
	return rv
}

func (c *Cell) SetMineContacts() {
	if c.Contents == Mine {
		c.Minecontacts = -1
		return
	}
	for _, cell := range c.Adjacent() {
		if cell.Contents == Mine {
			c.Minecontacts += 1
		}
	}
}

func (c *Cell) Edges() (top bool, bottom bool, left bool, right bool) {
	top, bottom, left, right = false, false, false, false
	if c.Y == 0 {
		top = true
	}
	if c.X == 0 {
		left = true
	}
	if c.X == c.Field.Width-1 {
		right = true
	}
	if c.Y == c.Field.Height-1 {
		bottom = true
	}
	return top, bottom, left, right
}

func (c *Cell) Render() (string, string, string) {
	header := ""
	mid := ""
	footer := ""
	me := fmt.Sprintf("%v", c)
	//length = len(colors.remove_color(me))
	length := len(me)

	top, bottom, left, right := c.Edges()
	if top {
		if left {
			header += "┌"
		} else {
			header += "┬"
		}
	} else {
		if left {
			header += "├"
		} else {
			header += "┼"
		}
	}
	for i := 0; i < length; i++ {
		header += "─"
	}
	if right {
		if top {
			header += "┐"
		} else {
			header += "┤"
		}
	}
	mid += "│" + me
	if right {
		mid += "│"
	}
	if bottom {
		if left {
			footer += "└"
		} else {
			footer += "┴"
		}
		for i := 0; i < length; i++ {
			footer += "─"
		}
		if right {
			footer += "┘"
		}
	}
	return header, mid, footer
}

func (c *Cell) String() string {
	return fmt.Sprintf("(%v, %v)", c.X, c.Y)
}
