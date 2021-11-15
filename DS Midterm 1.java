Question 1

public static Node deleteLastOccurrence(Node front, int item)
throws NoSuchElementException 
{
     Node target = null;
     Node current = front;
	 Node previous = null;
	 Node temp = null;

	 if(current.next == null)
	 {
	 	throw new NoSuchElementException("No such element exception");
	 }
     while(current.next != null)
	{
		if(current.data == item)
		{
			//previous -> target(last instance of current) -> temp 
			target = current;
			previous.next = target;
			temp = current.next;
		}

		current = current.next;
	}

	if(target == null)
	{
		return;
	}

	previous.next = temp.next;

	//previous.next -> temp
}

Question 2

public static void doRightSize(Node root)
{
​​​​​​​  	if(root.right() == null)
	{ 
		rightSize = 0;
	} 
	else
	{ 
		rightSize = 1+ doRightSize(root.left())+ doRight(root.right()) ;
	}
}



Question 4



