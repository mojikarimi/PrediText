function sub_but() {
    const element_button = document.getElementById("element_button");
    element_button.textContent = 'Pleas Wait... ';
    const element_span = document.createElement('span')
    element_span.setAttribute("class", "spinner-border spinner-border-sm")
    element_span.setAttribute("role", "status")
    element_span.setAttribute("aria-hidden", "true")
    element_button.appendChild(element_span)
    element_button.submit();
}