let selected_trope = [];
const MAX_TROPES = 5;
let stories = [];
let prompt_info = {
    selected_tropes : [],
    mc_name : "Alex",
    li_name: "Jordan",
    mc_pronouns : "Female",
    li_pronouns : "Male",
    dream_bible : {height: "tall", hair_color: "black", eye_color:"dark brown", aesthetic: "charming, slightly mysterious", interests: ""},
    spiciness : 0,
    humor : 0,
    angst : 0,
    warmth : 0
};
const story_popup = document.getElementById("story_popup");
const story_popup_text = document.getElementById("story_popup_text");
const generate_button = document.getElementById("generate_button");
const loading_popup = document.getElementById("loading_popup");

function toggleTrope(element, trope) {
    if (element.classList.contains("selected")) {
        element.classList.remove("selected");

        // remove trope from selected_trope
        selected_trope = selected_trope.filter(t => t !== trope);
    } else {
        if (selected_trope.length >= MAX_TROPES) {
            alert(`You can select up to ${MAX_TROPES} tropes only.`);
            return;
        }
        element.classList.add("selected");

        // add trope to selected_trope
        if (!selected_trope.includes(trope)) {
            selected_trope.push(trope);
        }
    }

}

function selectUserGender(usergender)   {
    prompt_info.mc_pronouns = usergender;
}

function selectPartnerGender(partnergender)   {
    prompt_info.li_pronouns = partnergender;
}

async function generateStory() {
    // Fetch user inputs
    if (selected_trope.length < 3 ){
        alert("Please select at least 3 tropes for your boyfriend!");
        return;
    }
    generate_button.disabled = true;
    loading_popup.classList.add("show_loading_popup");

    prompt_info.mc_name = document.getElementById("name_input").value;
    prompt_info.li_name = document.getElementById("partner_name_input").value;
    prompt_info.dream_bible["height"] = document.getElementById("height_select").value;
    prompt_info.dream_bible["hair_color"] = document.getElementById("hair_color_input").value;
    prompt_info.dream_bible["eye_color"] = document.getElementById("eye_color_input").value;
    prompt_info.dream_bible["aesthetic"] = document.getElementById("aesthetic_input").value;
    prompt_info.dream_bible["interests"] = document.getElementById("interests_input").value;
    prompt_info.spiciness = document.getElementById("tone1").value;
    prompt_info.humor = document.getElementById("tone2").value;
    prompt_info.angst = document.getElementById("tone3").value;
    prompt_info.warmth = document.getElementById("tone4").value;
    prompt_info.selected_tropes = selected_trope;
    
    const requestBody = {
        selected_tropes: prompt_info.selected_tropes,
        mc_name: prompt_info.mc_name,
        li_name: prompt_info.li_name,
        mc_pronouns: prompt_info.mc_pronouns,
        li_pronouns: prompt_info.li_pronouns,
        dream_bible: prompt_info.dream_bible,
        spiciness: parseInt(prompt_info.spiciness),
        humor: parseInt(prompt_info.humor),
        angst: parseInt(prompt_info.angst),
        warmth: parseInt(prompt_info.warmth)
    };

    try {
        // 5. Send POST request to FastAPI backend
        const response = await fetch("http://127.0.0.1:8000/generate_story", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const text = await response.text();
            alert("Backend error (" + response.status + "):\n" + text);
            return;
        }

        const raw = await response.text();
        console.log("RAW RESPONSE:", raw);
        //alert(raw);
        
        let data;
        try {
            data = JSON.parse(raw);
        } catch (e) {
            console.error("JSON parse error:", e);
            alert("Server returned invalid JSON.");
        }

        
        loading_popup.classList.remove("show_loading_popup");

        if (data.warnings && data.warnings.length > 0) {
            alert("Warning:\n" + data.warnings.join("\n") + "Try a new combination!" );
            //return;
        }
        //alert("Testing story:\n" + data.story);
        // // 6. Handle compatibility or backend errors
        // if (data.error) {
        //     alert(data.error);
        //     return;
        // }

        // 7. Show the story to the user
        stories.push(data.story);
        createNewStoryDiv();
        showStoryPopup(data.story);
        
        //document.getElementById("summary_box").textContent = data.story;
        generate_button.disabled = false;

    } catch (err) {
        generate_button.disabled = false;
        console.error("Error calling backend:", err);
        alert("Error calling backend:\n" + err);
    }

}

function closeStoryPopup() {
    story_popup.classList.remove("show_story_popup");
}

function showStoryPopup(text) {
    story_popup_text.textContent = text;
    story_popup.classList.add("show_story_popup"); 
}

const summary_box = document.getElementById("summary_box");
function createNewStoryDiv() {
    const storyDiv = document.createElement("div");
    storyDiv.classList.add("story_div");
    storyDiv.classList.add("gamja-flower-regular");
    storyDiv.textContent = "Story " + (stories.length) ;
    storyDiv.onclick = function() {
        showStoryPopup(stories[stories.length -1]);
    };
    summary_box.appendChild(storyDiv);
}