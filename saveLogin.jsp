<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1" import="com.cs336.pkg.*"%>
<%@ page import="java.io.*,java.util.*,java.sql.*"%>
<%@ page import="javax.servlet.http.*,javax.servlet.*" %>


<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
		
<title>Insert title here</title>
</head>
<body>
<%@ page import ="java.sql.*" %>
<% 
	String username = request.getParameter("username");
	String password = request.getParameter("password");

	ApplicationDB db = new ApplicationDB();	
	Connection con = db.getConnection();	
	Statement stmt = con.createStatement();
	
	ResultSet rs = stmt.executeQuery("select * from users where username='" + username + "'");
    if (rs.next()) {
    	out.println("This username is taken. <a href='createAccount.jsp'>try again</a>");
    } else {
    	int x = stmt.executeUpdate("insert into users values('" +username+ "', '" +password+ "')");
    	session.setAttribute("user", username); // the username will be stored in the session
        response.sendRedirect("success.jsp");

    	
    }
	
	
	
%>
</body>
</html>