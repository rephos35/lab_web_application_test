function changeImgInputtype() {
    img = document.getElementById("inputtype");
    if (img.src.match("manualinput")) {
        alert("                                        切換為 '輸入模式'");
        img.src = "static/image/search.png";
        img.title = "搜尋書本";
        // img.setAttribute("title", "搜尋書本");
        document.getElementById("input_list").innerHTML =
            "<form action='/manualinputbook' method='post' enctype='multipart/form-data'>\
            <label>書名:</label>\
            <input type='text' name='bookname' placeholder='書名'/>\
            <label>&ensp;作者:&nbsp;</label>\
            <input type='text' name='bookauthor' placeholder='作者'/>\
            <label>&ensp;出版社:</label>\
            <input type='text' name='bookpublisher' placeholder='出版社'/>\
            <label>&ensp;金額:</label>\
            <input type='text' name='bookcost' placeholder='$$$'/>\
            <label>&ensp;版本/備註:</label>\
            <input type='text' name='bookother' placeholder='版本/備註'/>\
            <input type='submit' name='save' value='儲存書本資訊'/>\
        </form>";

    } else {
        alert("                                        切換為 '查詢模式'");
        img.src = "static/image/manualinput.png";
        img.title = "手動輸入書本";
        // img.setAttribute("title", "手動輸入書本");
        document.getElementById("input_list").innerHTML =
            "<form action='/searchbook' method='post' enctype='multipart/form-data'>\
            <label>書名:</label>\
            <input type='text' name='bookname' placeholder='書名'/>\
            <label>&ensp;ISBN:</label>\
            <input type='text' name='bookisbn' placeholder='ISBN'/>\
            <label>&ensp;ISBN 照片:</label>\
            <input type='file' name='barcodefile'/>\
            <input type='submit' name='search' value='查詢書本'/>\
        </form>";
        
        
    }
    

}

function changeImgAddbook(id) {
    img = document.getElementById("search_book_"+id);
    alert(img.id);
    if (img.src.match("addedbook")) {
        img.src = "static/image/addbook.png";
    } else {
        img.src = "static/image/addedbook.png";
    }
}

function displayBlockDeletebook(){
    img.reload(location.reload());

}

