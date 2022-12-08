package main

import "fmt"

// They give a string and they ask you,
// how many substrings, that it contains all vowels, are there

func vowelDic(ch string) (bool, int) {
	switch ch {
	case "a":
		return true, 1
	case "e":
		return true, 10
	case "i":
		return true, 100
	case "o":
		return true, 1000
	case "u":
		return true, 10000
	default:
		return false, -1
	}
}

func test(value int) bool {
	for i := 0; i < 5; i++ {
		rest := value % 10
		if rest == 0 {
			return false
		}

		value /= 10
	}

	return true
}

func subCount(sub string, ch chan int) {
	q := make([][2]int, 0)

	for i := 0; i < len(sub)-5; i++ {

		value := 0
		for j := i; j-i < 5; j++ {
			ch := string(sub[j])
			_, v := vowelDic(ch)
			value += v
		}

		q = append(q, [2]int{i, value})
	}

	result := 0

	for len(q) > 0 {
		for i, tuple := range q {
			if test(tuple[1]) {
				result += len(sub) - 5 - tuple[0]
			} else if tuple[0]+6 < len(sub) {
				ch := string(sub[tuple[0]+6])
				_, v := vowelDic(ch)
				q[i] = [2]int{tuple[0] + 1, tuple[1] + v}
			}
		}
	}

	ch <- result
}

func vowelCount(str string) int {
	subStringPotentials := make([]string, 0)

	for i := 0; i < len(str); i++ {
		ch := string(str[i])
		isVowel, _ := vowelDic(ch)

		if isVowel {
			j := i
			for {
				if !isVowel {
					j--
					break
				}

				if j >= len(str) {
					break
				}

				ch := string(str[j])
				isVowel, _ = vowelDic(ch)
				j++
			}

			if j-i >= 5 {
				subStringPotentials = append(subStringPotentials, str[i:j])
			}
			i = j
		}
	}

	channelList := make([]chan int, 0)

	for _, sub := range subStringPotentials {
		ch := make(chan int)
		channelList = append(channelList, ch)
		go subCount(sub, ch)
	}

	result := 0

	for _, ch := range channelList {
		result += <-ch
	}

	return result
}

func main() {
	ask := "aaeiouxa"

	fmt.Println(vowelCount(ask))
}
