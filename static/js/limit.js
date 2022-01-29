// <input id="email" type="text" onkeydown="limit(this, 50);" onkeyup="limit(this, 50);">
// <label id="emailLen">0/50</label>

function limit(element, max_chars)
{
    if(element.value.length > max_chars) {
        element.value = element.value.substr(0, max_chars);
    }
    document.getElementById(element.id+"Len").innerHTML = element.value.length + "/" + max_chars;
}