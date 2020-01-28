function showEmail(element, cipherAttr, noisePattern) {
    element.innerText = element.getAttribute(cipherAttr).replace(noisePattern, '');
    element.removeAttribute('onmouseover');
    element.removeAttribute('onmousedown');
    element.removeAttribute('onclick');
}
