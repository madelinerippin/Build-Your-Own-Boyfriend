let selected_trope = null;

function selectItem(name) {
    if (selected_trope == null){ 
        selected_trope = name;
        const item = document.getElementById(name);
        item.classList.remove('trope_item');
        item.classList.add('selected_item');
    } else {
        const old_trope = document.getElementById(selected_trope);
        const new_trope = document.getElementById(name);

        old_trope.classList.remove('selected_item');
        old_trope.classList.add('trope_item');
        new_trope.classList.remove('trope_item');
        new_trope.classList.add('selected_item');
        selected_trope = name;
    }

    //Down here, change the summary box based off user selection too.
}