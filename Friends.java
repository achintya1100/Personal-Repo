package friends;

import java.util.ArrayList;
import structures.Queue;
import structures.Stack;

public class Friends {

    /**
     * Finds the shortest chain of people from p1 to p2.
     * Chain is returned as a sequence of names starting with p1,
     * and ending with p2. Each pair (n1,n2) of consecutive names in
     * the returned chain is an edge in the graph.
     * 
     * @param g Graph for which shortest chain is to be found.
     * @param p1 Person with whom the chain originates
     * @param p2 Person at whom the chain terminates
     * @return The shortest chain from p1 to p2. Null or empty array list if there is no
     *         path from p1 to p2
     */
    public static ArrayList < String > shortestChain(Graph g, String p1, String p2) 
    {
    	Queue <Person> chain = new Queue <Person> ();
        ArrayList <String> shortestChainList = new ArrayList <String> ();
        Person[] chainTraversal = new Person[g.members.length];
        boolean[] traversal = new boolean[g.members.length];
        int loc = g.map.get(p1);
        chain.enqueue(g.members[loc]);
        traversal[loc] = true;
        if(g == null || p1 == null || p2 == null) 
        {
            return null;
        }
        while(!chain.isEmpty()) 
        {
            Person x = chain.dequeue();
            traversal[g.map.get(x.name)] = true;
            Friend friend = x.first;
            if(friend == null) 
            {
                return null;
            }
            while(friend != null) 
            {
                if(!traversal[friend.fnum]) 
                {
                	chain.enqueue(g.members[friend.fnum]);
                    chainTraversal[friend.fnum] = x;
                	traversal[friend.fnum] = true;
                    if (g.members[friend.fnum].name.equals(p2)) 
                    {
                        x = g.members[friend.fnum];
                        while(!(x.name.equals(p1)))
                        {
                            shortestChainList.add(0, x.name);
                            x = chainTraversal[g.map.get(x.name)];
                        }
                        shortestChainList.add(0, p1);
                        return shortestChainList;
                    }
                }
                friend = friend.next;
            }
        }
        return null;
    }

    /**
     * Finds all cliques of students in a given school.
     * 
     * Returns an array list of array lists - each constituent array list contains
     * the names of all students in a clique.
     * 
     * @param g Graph for which cliques are to be found.
     * @param school Name of school
     * @return Array list of clique array lists. Null or empty array list if there is no student in the
     *         given school
     */
    public static ArrayList < ArrayList < String >> cliques(Graph g, String school) 
    {
        if (g == null || school == null) 
        {
            return null;
        }
        ArrayList <ArrayList <String >> list = new ArrayList <ArrayList <String>> ();
        return breathFirstSearch(g.members[0], list, g, school, new boolean[g.members.length]);
    }
    
    //Use Queue for BFS
    private static ArrayList <ArrayList <String>> breathFirstSearch(Person p, ArrayList <ArrayList<String>> list, Graph g, String s, boolean[] b)
    {
    	Person x = new Person();
    	Friend friend;
    	Queue <Person> q = new Queue <Person> ();
        ArrayList <String> returnList = new ArrayList <String> ();
        q.enqueue(p);
        b[g.map.get(p.name)] = true;
        if(!(p.school.equals(s)) || p.school == null) 
        {
            q.dequeue();
            for (int i = 0; i < b.length; i++) 
            {
                if (b[i]) 
                {
                    return breathFirstSearch(g.members[i], list, g, s, b);
                }
            }
        }
        while (!q.isEmpty()) 
        {
            x = q.dequeue();
            friend = x.first;
            returnList.add(x.name);
            while(friend != null) 
            {
                if(b[friend.fnum] == false) 
                {
                	if(g.members[friend.fnum].school.equals(s)) 
                    {
                        q.enqueue(g.members[friend.fnum]);
                    }
                	else
                	{
                		
                	}
                    b[friend.fnum] = true;
                }
                friend = friend.next;
            }
        }
        if (returnList.isEmpty() && list.isEmpty() == false) 
        {

        } 
        else 
        {
            list.add(returnList);
        }
        for (int i = 0; i < b.length; i++) 
        {
            if (b[i] == false) 
            {
                return breathFirstSearch(g.members[i], list, g, s, b);
            }
        }
        return list;
    }

    

    /**
     * Finds and returns all connectors in the graph.
     * 
     * @param g Graph for which connectors needs to be found.
     * @return Names of all connectors. Null or empty array list if there are no connectors.
     */
    public static ArrayList < String > connectors(Graph g) {
        if (g == null) 
        {
            return null;
        }
        ArrayList <String> list = new ArrayList <String> ();
        boolean[] b = new boolean[g.members.length];
        ArrayList <String> beforeList = new ArrayList <String> ();
        int[] x = new int[g.members.length];
        int[] y = new int[g.members.length];
        for (int i = 0; i < g.members.length; i++) 
        {
            if (!b[i]) 
            {
                list = depthFirstSearch(g.members[i], g, list, x, new int[] {0,0}, b, true, beforeList, y);
            }
        }
        return list;
    }
   
    //Use Stack for DFS
    private static ArrayList <String> depthFirstSearch(Person p, Graph g, ArrayList <String> list, int[] num, int[] i, boolean[] b, boolean bo, ArrayList <String> reverseList, int[] arr)
    {
        b[g.map.get(p.name)] = true;
        Friend friend = p.first;
        num[g.map.get(p.name)] = i[0];
        arr[g.map.get(p.name)] = i[1];
        while(friend != null) 
        {
            if (!b[friend.fnum]) 
            {
                i[0] = i[0] + 1;
                i[1] = i[1] + 1;
                list = depthFirstSearch(g.members[friend.fnum], g, list, num, i, b, false, reverseList, arr);
                if (num[g.map.get(p.name)] <= arr[friend.fnum]) 
                {
                    if (reverseList.contains(p.name) && (!list.contains(p.name)) || (bo == false) && (!list.contains(p.name))) 
                    {
                    	list.add(p.name);
                    }
                } 
                else 
                {
                    int first = arr[g.map.get(p.name)];
                    int second = arr[friend.fnum];
                    if (first > second) 
                    {
                        arr[g.map.get(p.name)] = second;
                    } 
                    else
                    {
                    	arr[g.map.get(p.name)] = first;
                    }
                }
                reverseList.add(p.name);
            } 
            else 
            {
                int third = arr[g.map.get(p.name)];
                int fourth = num[friend.fnum];
                if (third > fourth) 
                {
                    arr[g.map.get(p.name)] = fourth;
                } 
                else 
                {
                	arr[g.map.get(p.name)] = third;
                }
            }
            friend = friend.next;
        }
        return list;
    }
}