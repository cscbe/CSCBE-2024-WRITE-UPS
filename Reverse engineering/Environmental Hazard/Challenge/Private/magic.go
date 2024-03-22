package main

import (
	"fmt"
	"os"
)

func main() {
	if is_floor_dry() {
		fmt.Println("CSC{Y3AH_upX_15_n0T_S3cURitY}")
	} else {
		fmt.Println("Whoops! I slipped, sorry, I dropped the flag :(")
	}

}

func is_floor_dry() bool {
	_, is_floor_dry := os.LookupEnv("IS_FLOOR_DRY")
	return is_floor_dry
}
