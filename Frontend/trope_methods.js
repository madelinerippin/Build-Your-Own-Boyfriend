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
    warmth : 0,
    selected_tropes_and_beats: []
};
const story_popup = document.getElementById("story_popup_dark_screen");
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

    let story_beats_list = []
    for(let i = 0; i < selected_trope.length; i++){
      const trope_data = story_beats_data.find(trope_object => trope_object.name === selected_trope[i]);
      let new_beats_dict = {};
      new_beats_dict["beats"] = trope_data.beats;
      story_beats_list.push(new_beats_dict);
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
    prompt_info.selected_tropes_and_beats = story_beats_list;
    
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
        warmth: parseInt(prompt_info.warmth),
        custom_beats: prompt_info.selected_tropes_and_beats
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
            generate_button.disabled = false;
            return;
        }
        //alert("Testing story:\n" + data.story);
        // // 6. Handle compatibility or backend errors
        // if (data.error) {
        //     alert(data.error);
        //     return;
        // }

        // 7. Show the story to the user
        stories.push(data.story);
        createNewStoryDiv(stories.length - 1);
        showStoryPopup(data.story);
        
        //document.getElementById("summary_box").textContent = data.story;
        generate_button.disabled = false;

    } catch (err) {
        generate_button.disabled = false;
        //Not tested since not sure how to force this lol
        loading_popup.classList.remove("show_loading_popup");
        console.error("Error calling backend:", err);
        alert("Error calling backend:\n" + err);
    }

}

function closeStoryPopup() {
    // story_popup.classList.remove("show_story_popup");
    story_popup.style.visibility = "hidden";
}

function showStoryPopup(text) {
    story_popup_text.textContent = text;
    // story_popup.classList.add("show_story_popup"); 
    story_popup.style.visibility = "visible";
}

const summary_box = document.getElementById("summary_box");
function createNewStoryDiv(index) {
    const storyDiv = document.createElement("div");
    storyDiv.classList.add("story_div");
    storyDiv.classList.add("gamja-flower-regular");
    storyDiv.textContent = "Story " + (stories.length) ;
    storyDiv.onclick = function() {
        showStoryPopup(stories[index]);
    };
    summary_box.appendChild(storyDiv);
    console.warn(stories);
}

function closeBeatsPopup() {

    const popup_box = document.getElementById("story_beats_popup");
    popup_box.style.visibility = "hidden";

}

const story_beats_data = [
  {
    "name": "Enemies to Lovers",
    "beats": [
      "Hostile or snarky first encounter",
      "Petty rivalry or sabotage",
      "Forced proximity or joint task",
      "Moment of unexpected vulnerability",
      "Shift to jealousy or awareness",
      "Breaking point confession or kiss"
    ],
    "lexical_markers": [
      "You drive me insane.",
      "Stop looking at me like that.",
      "I can't stand you...but I can't stop thinking about you.",
      "Why are you suddenly being nice to me?",
      "This doesn't mean I like you.",
      "You're impossible...and it's annoying how much I notice you."
    ]
  },
  {
    "name": "Friends to Lovers",
    "beats": [
      "Comfortable friendship dynamic",
      "New awareness of attraction",
      "Jealousy or shift in boundaries",
      "Accidental intimacy",
      "Confession or emotional risk",
      "Realizing the relationship can evolve"
    ],
    "lexical_markers": [
      "When did you start looking at me like that?",
      "We've always been close...but this feels different.",
      "You're the one person I can't lose.",
      "Why does it feel weird seeing you with someone else?",
      "Don't make me fall for you. Not like this."
    ]
  },
  {
    "name": "Forbidden Love",
    "beats": [
      "Recognition of the boundary",
      "Unwanted attraction",
      "Secret meetings or stolen moments",
      "Risk of exposure",
      "Conflict between desire and consequences",
      "Courage or sacrifice"
    ],
    "lexical_markers": [
      "We can't do this...but I want to.",
      "If someone sees us—",
      "I shouldn't touch you. I know that.",
      "You make me forget every rule I'm supposed to follow.",
      "Say the word and I'll walk away. Just say it.",
      "You're worth the risk."
    ]
  },
  {
    "name": "Fake Relationship",
    "beats": [
      "Agreement to pretend",
      "Public displays of affection",
      "Blurry boundaries",
      "Jealousy or protectiveness",
      "Accidental intimacy",
      "Confession or realization"
    ],
    "lexical_markers": [
      "We should practice… to make it convincing.",
      "That didn't feel fake.",
      "You're enjoying this way too much.",
      "If we're pretending, why does my heart feel like this?",
      "One more kiss. For the plan. Right?"
    ]
  },
  {
    "name": "Grumpy and Sunshine",
    "beats": [
      "Clashing personalities",
      "Sunshine softens grumpy",
      "Grumpy protects sunshine",
      "Private emotional opening",
      "Growing interdependence",
      "Mutual realization"
    ],
    "lexical_markers": [
      "Why are you always smiling at me?",
      "Stop trying to make me laugh—it's working.",
      "You look at me like I'm worth something.",
      "I don't know how to be gentle...but I want to try for you."
    ]
  },
  {
    "name": "Love Triangle",
    "beats": [
      "Establishing both connections",
      "Conflicted attraction",
      "Jealousy from both sides",
      "Moments of clarity with each",
      "Emotional breaking point",
      "Final decision"
    ],
    "lexical_markers": [
      "I can't choose. Not yet.",
      "You make me feel safe… but he makes my heart race.",
      "This isn't fair to any of us.",
      "Why does it hurt seeing you with them?",
      "I have to follow my heart, even if it breaks yours."
    ]
  },
  {
    "name": "Best Friend's Brother",
    "beats": [
      "Long-standing familiarity",
      "New physical or emotional awareness",
      "Secret flirtation",
      "Caught or nearly caught",
      "Conversation about loyalty",
      "Acceptance or confrontation"
    ],
    "lexical_markers": [
      "If your brother finds out—",
      "This is a bad idea. A really hot, really bad idea.",
      "We can't let them see us together.",
      "You're off-limits...but that never stopped me.",
      "I've wanted you longer than you think."
    ]
  },
  {
    "name": "Second Chance Romance",
    "beats": [
      "Unexpected reunion",
      "Old wounds resurfacing",
      "Lingering chemistry",
      "Rehashing the past",
      "Moment of clarity or apology",
      "Recommitment"
    ],
    "lexical_markers": [
      "I didn't think I'd see you again.",
      "You still know exactly how to get to me.",
      "I never stopped wanting you.",
      "I'm scared you'll break my heart again.",
      "Maybe this time we can get it right."
    ]
  },
  {
    "name": "Age Gap",
    "beats": [
      "Recognition of age difference",
      "Reluctance or denial",
      "Growing chemistry",
      "Power dynamic discussion",
      "External judgment or conflict",
      "Commitment despite disparity"
    ],
    "lexical_markers": [
      "You're too young for me… or at least you should be.",
      "I shouldn't want someone your age.",
      "You make me forget how old I am.",
      "This feels wrong, but it also feels right.",
      "Age doesn't scare me. Losing you does."
    ]
  },
  {
    "name": "Secret Billionaire",
    "beats": [
      "Meeting under ordinary circumstances",
      "Growing connection",
      "Hints of hidden lifestyle",
      "Truth revealed accidentally or intentionally",
      "Betrayal or uncertainty",
      "Reconciliation and trust"
    ],
    "lexical_markers": [
      "There's something I haven't told you.",
      "I didn't want you to like me because of the money.",
      "I wanted one person who saw *me*.",
      "I'm still the same person you met.",
      "Let me prove I'm worth trusting."
    ]
  }
]

const story_beats_popup = document.getElementById("story_beats_popup");
const story_beats_title = document.getElementById("title_beat_box");
const add_beat_button = document.getElementById("add_beat_icon");
const beat_form = document.getElementById("beatsForm");
const BEAT_MIN = 3;
const BEAT_MAX = 6;
var current_num_beats = 0;

function fillContainer(trope){
    // Grab the 6 story tropes from the data, create a box for each of them and display them.
    // Display the text as textboxes that the user can edit.
    const trope_data = story_beats_data.find(trope_object => trope_object.name === trope);
    current_num_beats = trope_data.beats.length;

    for (let i = 0; i < trope_data.beats.length; i++) {
        
        const newBeat = document.createElement("div");
        newBeat.classList.add("beat_item");
        const beatNumber = document.createElement("div");
        beatNumber.classList.add("center_stuff");
        beatNumber.classList.add("gamja-flower-regular");
        beatNumber.id = "beatID";
        beatNumber.style.fontSize = 48;
        beatNumber.innerText = "Beat " + (i+1);
        const beatInfo = document.createElement("textarea");
        beatInfo.classList.add("text_area");
        beatInfo.rows = 1;
        beatInfo.name = `beat_${i}`;
        beatInfo.value = trope_data.beats[i];
        const removeButtonContainer = document.createElement("div");
        removeButtonContainer.classList.add("center_stuff");
        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.classList.add("remove_beat");
        removeButton.classList.add("center_stuff");
        removeButton.innerText = "X";
        removeButton.addEventListener("click", (e) => {
            if (current_num_beats <= BEAT_MIN) {
              return;
            }else{
                newBeat.remove();
                updateBeatIndexes();
                current_num_beats = current_num_beats - 1;
            }
        });
        newBeat.appendChild(beatNumber);
        newBeat.appendChild(beatInfo);
        removeButtonContainer.appendChild(removeButton);
        newBeat.appendChild(removeButtonContainer);
        beat_form.appendChild(newBeat);
    };
}

var current_trope = '';

function openBeatsPopup(trope) {
    event.stopPropagation();
    story_beats_popup.style.visibility = "visible";
    story_beats_title.innerText = trope;
    current_trope = trope;
    beat_form.innerHTML = "";
    fillContainer(trope);

}

function updateBeatIndexes() {
    const beats = document.querySelectorAll(".beat_item");
    beats.forEach((beat, i) => {
        beat.querySelector("#beatID").innerText = `Beat ${i + 1}`;
    });
}

add_beat_button.addEventListener("click", () => {
  console.log("hit");
  const trope_data = story_beats_data.find(trope_object => trope_object.name === current_trope);
  if (current_num_beats < BEAT_MAX){
      current_num_beats = current_num_beats + 1;
      const newBeat = document.createElement("div");
      newBeat.classList.add("beat_item");
      const beatNumber = document.createElement("div");
      beatNumber.classList.add("center_stuff");
      beatNumber.classList.add("gamja-flower-regular");
      beatNumber.id = "beatID";
      beatNumber.style.fontSize = 48;
      beatNumber.innerText = "Beat " + (current_num_beats);
      const beatInfo = document.createElement("textarea");
      beatInfo.classList.add("text_area");
      beatInfo.rows = 1;
      beatInfo.name = `beat_${current_num_beats}`;
      beatInfo.value = "";
      console.log(trope_data.beats);
      const removeButtonContainer = document.createElement("div");
      removeButtonContainer.classList.add("center_stuff");
      const removeButton = document.createElement("button");
      removeButton.type = "button";
      removeButton.classList.add("remove_beat");
      removeButton.classList.add("center_stuff");
      removeButton.innerText = "X";
      removeButton.addEventListener("click", (e) => {
          if (current_num_beats <= BEAT_MIN) {
            return;
          }else{

              newBeat.remove();
              updateBeatIndexes();
              current_num_beats = current_num_beats - 1;
          }
      });

      newBeat.appendChild(beatNumber);
      newBeat.appendChild(beatInfo);
      removeButtonContainer.appendChild(removeButton);
      newBeat.appendChild(removeButtonContainer);
      beat_form.appendChild(newBeat);
    }else{
      return;
    }
  });

function saveBeats() {
    const trope_data = story_beats_data.find(trope_object => trope_object.name === current_trope);

    const form = document.getElementById("beatsForm");
    const inputs = form.querySelectorAll("textarea");

    let emptyFound = false;
    inputs.forEach(input => {
        if (input.value.trim() === "") {
            emptyFound = true;
        }
    });

    if (emptyFound) {
        alert("All beats must be filled before saving!");
        return;
    }

    trope_data.beats = [];
    inputs.forEach(input => {
        trope_data.beats.push(input.value.trim());
    });

    console.log("Saved:", trope_data.beats);

    closeBeatsPopup()
}