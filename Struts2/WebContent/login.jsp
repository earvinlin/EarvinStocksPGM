<%@ page language="java"  pageEncoding="UTF-8"%>
<%@ taglib prefix="s" uri="/struts-tags" %>		<!-- 匯入Struts 2標籤庫-->
<style type="text/css">*{font-size:12px;}</style>
<html><body>
	<div style=" margin:30px 50px 20px 50px; text-align:center">
        <div style="font-size:14px; font-weight:bold">使用者登入</div>
        <div>
            <s:form action="checkLogin" namespace="/login">
            <s:textfield name="username" style="font-size:12px; width:120px;" label="登入名稱" />
            <s:password name="password" style="font-size:12px; width:120px;" label="登入密碼" />
            <s:submit value=" 登 錄 " />
            </s:form>
        </div>
	</div>
</body></html>
