package main

import "fmt"

func cmp(a [2]int32, b [2]int32) ([2]int32, [2]int32) {
	if a[0] < b[0] {
		return a, b
	}

	if a[0] > b[0] {
		return b, a
	}

	if a[1] < b[1] {
		return a, b
	}

	return b, a
}

func binarySort(arr [][2]int32, ch chan [][2]int32) {
	if len(arr) == 2 {
		a, b := cmp(arr[0], arr[1])
		ch <- [][2]int32{a, b}
		return
	}

	if len(arr) == 1 {
		ch <- arr
		return
	}

	cha := make(chan [][2]int32)
	chb := make(chan [][2]int32)

	go binarySort(arr[0:len(arr)/2], cha)
	go binarySort(arr[len(arr)/2:], chb)

	a := <-cha
	b := <-chb

	result := make([][2]int32, 0)

	indexA, indexB := 0, 0
	for indexA < len(a) && indexB < len(b) {
		_a, _ := cmp(a[indexA], b[indexB])

		if _a == a[indexA] {
			indexA++
		} else {
			indexB++
		}

		result = append(result, _a)
	}

	for indexA < len(a) {
		result = append(result, a[indexA])
		indexA++
	}

	for indexB < len(b) {
		result = append(result, b[indexB])
		indexB++
	}

	ch <- result
	return

}

func insertionSort(arr []int32) int32 {
	arr_map := make([][2]int32, 0)

	for i := 0; i < len(arr); i++ {
		arr_map = append(arr_map, [2]int32{arr[i], int32(i)})
	}

	ch := make(chan [][2]int32)
	go binarySort(arr_map, ch)
	arr_map = <-ch

	var result int32 = 0
	for i := 0; i < len(arr); i++ {

		fmt.Println(arr_map[i][0], arr_map[i][1], i)
		sum := arr_map[i][1] - int32(i)

		if sum == 0 && i+1 < len(arr) && arr_map[i][1] > arr_map[i+1][1] {
			sum = 2
		}

		if sum < 0 {
			sum *= -1
		}

		result += sum
	}

	return result / 2
}

func main() {
	var input []int32
	input = []int32{12, 15, 1, 5, 6, 14, 11}

	fmt.Println(insertionSort(input))
}

// 0, 	1, 	2,	3,	4, 	5, 	6
// 12, 15,  1,  5,  6, 14, 11
// 1,  12, 15,  5,  6, 14, 11 -> 2
// 1, 	5, 12, 15,  6, 14, 11 -> 2
// 1, 	5,  6, 12, 15, 14, 11 -> 2
// 1, 	5,  6, 12, 14, 15, 11 -> 1
// 1, 	5,  6, 11, 12, 14, 15 -> 3

// 2,	2,	2,	3,	4, 	0	5
