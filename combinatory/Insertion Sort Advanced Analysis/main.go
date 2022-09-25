package main

type Node struct {
	RightNode *Node
	LeftNode  *Node
	value     int32
	count     int
}

func createNewNode(value int32) *Node {
	result := Node{
		RightNode: nil, // less value
		LeftNode:  nil, // hide value
		value:     value,
		count:     0,
	}

	return &result
}

func (n *Node) CountSteepToEnd() int32 {
	var leftValue int32 = 0
	if n.LeftNode == nil {
		leftValue = n.LeftNode.CountSteepToEnd()
	}

	return int32(n.count) + leftValue
}

func (n *Node) AddNewValue(value int32) *Node {
	switch {
	case n.value == value:
		n.count += 1

	case n.value < value && n.LeftNode != nil:
		n.LeftNode = n.LeftNode.AddNewValue(value)

	case n.value < value && n.LeftNode == nil:
		n.LeftNode = createNewNode(value)

	case n.value > value && n.RightNode != nil:
		n.RightNode = n.RightNode.AddNewValue(value)

	case n.value > value && n.RightNode != nil:
		n.RightNode = createNewNode(value)
	}

	return n
}

func (n *Node) FindInsertionNode(value int32) *Node {
	switch {
	case n.value == value:
		return n.LeftNode

	case n.value < value && n.RightNode == nil:
		return n
	case n.value > value:
		return n.RightNode.FindInsertionNode(value)

	case n.value < value && n.LeftNode.value < value:
		return n.LeftNode.FindInsertionNode(value)

	default:
		return n.LeftNode

	}
}

func insertionSort(arr []int32) int32 {
	len_arr := len(arr)
	if len_arr == 0 {
		return 0
	}

	avlTree := createNewNode(arr[0])
	var result int32 = 0
	var maxPivot int32 = -1

	for i := 1; i < len_arr; i++ {
		avlTree = avlTree.AddNewValue(arr[i])

		if maxPivot >= arr[i] {
			maxPivot = arr[i]
			continue
		}

		result += avlTree.FindInsertionNode(arr[i]).CountSteepToEnd()
	}

	return result

}
