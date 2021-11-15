package poly;

import java.io.IOException;
import java.util.Scanner;

/**
 * This class implements evaluate, add and multiply for polynomials.
 * 
 * @author Achintya Singh
 *
 */
public class Polynomial 
{
	
	/**
	 * Reads a polynomial from an input stream (file or keyboard). The storage format
	 * of the polynomial is:
	 * <pre>
	 *     <coeff> <degree>
	 *     <coeff> <degree>
	 *     ...
	 *     <coeff> <degree>
	 * </pre>
	 * with the guarantee that degrees will be in descending order. For example:
	 * <pre>
	 *      4 5
	 *     -2 3
	 *      2 1
	 *      3 0
	 * </pre>
	 * which represents the polynomial:
	 * <pre>
	 *      4*x^5 - 2*x^3 + 2*x + 3 
	 * </pre>
	 * 
	 * @param sc Scanner from which a polynomial is to be read
	 * @throws IOException If there is any input error in reading the polynomial
	 * @return The polynomial linked list (front node) constructed from coefficients and
	 *         degrees read from scanner
	 */
	public static Node read(Scanner sc) 
	throws IOException {
		Node poly = null;
		while (sc.hasNextLine()) {
			Scanner scLine = new Scanner(sc.nextLine());
			poly = new Node(scLine.nextFloat(), scLine.nextInt(), poly);
			scLine.close();
		}
		return poly;
	}
	
	/**
	 * Returns the sum of two polynomials - DOES NOT change either of the input polynomials.
	 * The returned polynomial MUST have all new nodes. In other words, none of the nodes
	 * of the input polynomials can be in the result.
	 * 
	 * @param poly1 First input polynomial (front of polynomial linked list)
	 * @param poly2 Second input polynomial (front of polynomial linked list
	 * @return A new polynomial which is the sum of the input polynomials - the returned node
	 *         is the front of the result polynomial
	 */
	public static Node add(Node poly1, Node poly2) 
	{
		/** COMPLETE THIS METHOD **/
		if(poly1 == null && poly2 == null)
		{
			return null;
		}
		Node first = null;
		Node second = null;
		Node head = null;
		while (poly1 != null && poly2 != null)
		{
			if(poly1.term.degree == poly2.term.degree)
			{
				second = new Node(poly1.term.coeff + poly2.term.coeff, poly1.term.degree, null);
				if(first != null)
				{
					first.next = second;
				}
				else
				{
					head = second;
				}
				poly1 = poly1.next;
				poly2 = poly2.next;
				first = second;
			}
			else if(poly1.term.degree < poly2.term.degree)
			{
				second = new Node(poly1.term.coeff, poly1.term.degree, null);
				if(first != null)
				{
					first.next = second;
				}
				else
				{
					head = second;
				}
				poly1 = poly1.next;
				first = second;
			}
			else if(poly1.term.degree > poly2.term.degree)
			{
				second = new Node(poly2.term.coeff, poly2.term.degree, null);
				if(first != null)
				{
					first.next = second;
				}
				else
				{
					head = second;
				}
				poly2 = poly2.next;
				first = second;
			}
		}
		if(poly1 != null)
		{
			while (poly1 != null)
			{
				second = new Node(poly1.term.coeff, poly1.term.degree, null);
				if(first != null)
				{
					first.next = second;
				}
				else
				{
					head = second;
				}
				poly1 = poly1.next;
				first = second;
			}
		}
		else if(poly2 != null)
		{
			while(poly2 != null)
			{
				second = new Node(poly2.term.coeff, poly2.term.degree, null);
				if(first != null)
				{
					first.next = second;
				}
				else
				{
					head = second;
				}
				poly2 = poly2.next;
				first = second;
			}
		}
		Node temp = null;
		second = head;
		while(second != null)
		{
			if(second.term.coeff == 0)
			{
				if(second != head)
				{
					temp.next = second.next;
				}
				else
				{
					head = second.next;
				}
			}
			else
			{
				temp = second;
			}
			second = second.next;
		}
		return head;
	}
	
	/**
	 * Returns the product of two polynomials - DOES NOT change either of the input polynomials.
	 * The returned polynomial MUST have all new nodes. In other words, none of the nodes
	 * of the input polynomials can be in the result.
	 * 
	 * @param poly1 First input polynomial (front of polynomial linked list)
	 * @param poly2 Second input polynomial (front of polynomial linked list)
	 * @return A new polynomial which is the product of the input polynomials - the returned node
	 *         is the front of the result polynomial
	 */
	public static Node multiply(Node poly1, Node poly2) 
	{
		/** COMPLETE THIS METHOD **/
		Node head = null;
		if(poly1 == null || poly2 == null)
		{
			return head;
		}
		Node pointer = null;
		Node product = null;	// good
		for(Node second = poly2; second != null; second = second.next)
		{
			for(Node temp = poly1; temp != null; temp = temp.next)
			{
				Node node = new Node(temp.term.coeff * second.term.coeff, temp.term.degree + second.term.degree, null);	//good
				if(pointer != null)	//good
				{
					pointer.next = node;
				}
				else
				{
					head = node;
				}
				pointer = node;
			}
			product = add(product, head);
			head = null;
			pointer = null;
		}
		return product;
	}

    static float sum(Node head)
    {
		float answer = 0;
		Node sumNode = head;
        while(sumNode != null)
        {
			answer += sumNode.term.coeff;
			sumNode = sumNode.next;
		}
		return answer;
	} 
    
    /** Error - Method has to return type float(?)
    private static float traversalSum(Node head)
    {
        float sum = 0;
        if(head == null)
        {
            return sum;
        }
        sum += head.term.coeff;

        traversalSum(head.next);
    }

    */

	/**			
	 * Evaluates a polynomial at a given value.
	 * @param poly Polynomial (front of linked list) to be evaluated
	 * @param x Value at which evaluation is to be done
	 * @return Value of polynomial p at x
	 */
	public static float evaluate(Node poly, float x) 
	{
		/** COMPLETE THIS METHOD **/
		if(poly == null)
		{
			return 0;
		}
		double power = 0.0;
		String powerAsString = "";
		float powerAsFloat = 0;
		Node evaluateReturn = null;
		while(poly != null)
		{
			power = Math.pow(x, poly.term.degree);
			powerAsString = Double.toString(power);
			powerAsFloat = Float.parseFloat(powerAsString);
			evaluateReturn = new Node(poly.term.coeff * powerAsFloat, 0, evaluateReturn);
			poly = poly.next;
		}
		return sum(evaluateReturn);
	}
	
	/**
	 * Returns string representation of a polynomial
	 * 
	 * @param poly Polynomial (front of linked list)
	 * @return String representation, in descending order of degrees
	 */
	public static String toString(Node poly) {
		if (poly == null) {
			return "0";
		} 
		
		String retval = poly.term.toString();
		for (Node current = poly.next ; current != null ;
		current = current.next) {
			retval = current.term.toString() + " + " + retval;
		}
		return retval;
	}	
}