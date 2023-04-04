
/**
 * Adds a loading spinner to a given div and returns a function that removes it
 * @param {string} divId - The ID of the div to add the loading spinner to
 * @param {number} opacity - The opacity of the loading spinner (default is 0.5)
 * @returns {function} A function that removes the loading spinner from the div
 */
const setDivLoading = function (divId, opacity = 0.5) {
    const divToLoad = document.getElementById(divId);
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('loading');
    loadingDiv.innerHTML = '<img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif">';
    divToLoad.appendChild(loadingDiv);
    return function () {
        divToLoad.removeChild(loadingDiv);
    }
}


