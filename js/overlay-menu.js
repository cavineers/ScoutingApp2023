

/**
 * Creates a popup menu to overlay onto the page.
 * @param {string} width css value for width of the menu. Default is 50%
 * @param {string} height css value for height of the menu. Defualt is 50%
 * @returns {HTMLDivElement} Menu container from which the menu can also be retrieved.
 */
function createMenu(width, height) {
    //create menu container (darkened background)
    closeMenu = (e) => {
        if (e.button != 0) //if not left click
            return;

        container.remove(); //remove menu and container from the page
    };

    var container = document.createElement("div");
    container.classList.add("menu-container");

    //create clickable section that closes menu behind the menu
    var bg = document.createElement("div");
    bg.style.position = "fixed";
    bg.style.width = "100%";
    bg.style.height = "100%";
    bg.addEventListener("click", closeMenu);


    //create menu
    var menu = document.createElement("div");
    menu.style.position = "absolute";
    menu.classList.add("menu", getThemeName());

    //create close button
    var closeButton = document.createElement("button");
    closeButton.addEventListener("click", closeMenu);
    closeButton.classList.add("menu-close-button", getThemeName());
    //add button image (src controlled by css)
    var closeImg = document.createElement("img");
    closeImg.alt = "Close";
    closeButton.appendChild(closeImg);


    if (width)
        menu.style.width = width;
    if (height)
        menu.style.height = height;


    //add elements
    menu.appendChild(closeButton);
    container.appendChild(bg);
    container.appendChild(menu);
    
    return container;
}

/**
 * Creates a popup menu to overlay onto the page and displays it.
 * @param {HTMLElement} addTo The element which the popup will become the child of. Default is document.body.
 * @param {string} width css value for width of the menu. Default is 50%
 * @param {string} height css value for height of the menu. Defualt is 50%
 * @returns {HTMLDivElement} Menu container from which the menu can also be retrieved.
 */
function addMenu(addTo, width, height) {
    container = createMenu(width, height);

    //Add menu
    (addTo?addTo:document.body).appendChild(container);

    return container;
}