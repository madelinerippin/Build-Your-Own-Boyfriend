#ok this is the best one with decisions and full story output and also allowed
#the beat modification which is good

import json
import random
import openai
from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()
#dictionary to get main character and love interest's pronouns after user input
PRONOUNS = {
    "male": {"subj": "he", "obj": "him", "poss": "his"},
    "female": {"subj": "she", "obj": "her", "poss": "her"},
    "nonbinary": {"subj": "they", "obj": "them", "poss": "their"}
}

#dictionary to ensure the user doesn't do friends to lovers and enemies to lovers in the same generation
#this can be fixed because there can be a lot more combos than what this is allowing
"""compatible_tropes = {
    "Enemies to Lovers": ["Grumpy and Sunshine", "Fake Relationship", "Forbidden Love"],
    "Friends to Lovers": ["Second Chance Romance", "Best Friend's Brother"],
    "Forbidden Love": ["Love Triangle", "Secret Billionaire", "Enemies to Lovers"],
    "Fake Relationship": ["Grumpy and Sunshine", "Enemies to Lovers", "Secret Billionaire"],
    "Grumpy and Sunshine": ["Fake Relationship", "Enemies to Lovers", "Age Gap"],
    "Love Triangle": ["Forbidden Love", "Secret Billionaire"],
    "Best Friend's Brother": ["Friends to Lovers", "Second Chance Romance"],
    "Second Chance Romance": ["Friends to Lovers", "Best Friend's Brother"],
    "Age Gap": ["Grumpy and Sunshine", "Secret Billionaire"],
    "Secret Billionaire": ["Forbidden Love", "Fake Relationship", "Age Gap", "Love Triangle"]
}"""


#loading in JSONS
#tropes.json: lists each trope and their corresponding overview (not used), beats (need),
#semantic key words (not used), lexical markers (used)
#example_quotes_per_trope.json: gives 9 example quotes from each trope that model can use for dialogue ideas (used)


with open("tropes.json", "r", encoding="utf-8") as f:
    trope_data = json.load(f)
trope_dict = {t["name"]: t for t in trope_data}

with open("example_quotes_per_trope.json", "r", encoding="utf-8") as f:
    snippet_db = json.load(f)


#need to figure out a way to set up a .env so this isn't hard coded
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # insert your key here or use env variable

#all of the user input sections!! There are default options right now if the user doesn't fill something out
#but should change that to make required sections say "please enter a valid name", etc

#the user's name and gender (thinking this can be the first page)
'''
mc_name = input("Enter the main character's name: ").strip() or "Alex"
mc_gender = input("Choose the main character's gender (male/female/nonbinary): ").strip().lower() or "female"
mc_pronouns = PRONOUNS.get(mc_gender, PRONOUNS["female"])

#the love interest's name and gender (thinking all this can be the 2nd page)
li_name = input("Enter the love interest's name: ").strip() or "Jordan"
li_gender = input("Choose the love interest's gender (male/female/nonbinary): ").strip().lower() or "male"
li_pronouns = PRONOUNS.get(li_gender, PRONOUNS["male"])

#the love interest's details (height, hair color, eye color, aesthetic, interests)
#should we add anything else? tried to keep it to more physical attributes so it wouldn't
#affect what tropes the user chose
#this also has defaults for now, not sure if we should make it required or not?
#also should probably do more validation for the aesthetic and interests since they are , separated
#also was told that it would be a good idea to have examples for aesthetic/vibe and interests/hobbies

print("\nEnter dream love interest details (leave blank for defaults):")
li_height = input("Height: ").strip() or "tall"
li_hair = input("Hair color: ").strip() or "dark brown"
li_eyes = input("Eye color: ").strip() or "green"
li_aesthetic = input("Aesthetic/vibe (separate by commas) (ex. mysterious, golden retriever, vampire): ").strip().split(",") or ["charming", "slightly mysterious"]
li_interests = input("Interests/hobbies (separate by commas) (cats, soccer, computer science): ").strip().split(",") or []

dream_bible = {
    "height": li_height,
    "hair_color": li_hair,
    "eye_color": li_eyes,
    "aesthetic": [a.strip() for a in li_aesthetic if a.strip()],
    "interests": [i.strip() for i in li_interests if i.strip()]
}

#this allows the user to adjust how spicy they want the story (thinking this can be the 3rd page)
#should we add anything else? I'd like to keep spiciness and angst :)
#defaults to 5 otherwise, this should be kept

print("\nSet the tone for the story (enter values between 1–10):")
spiciness = int(input("Spiciness: ") or 5)
humor = int(input("Humor: ") or 5)
angst = int(input("Angst: ") or 5)
warmth = int(input("Warmth: ") or 5)
'''
#checks if the tropes the user selected are compatible with each other
#currently don't have a limit on the number of tropes the user selects so long as they're compatible
#idk if we should have that tho?
"""def is_compatible(selected_tropes, new_trope):
    for t in selected_tropes:
        if new_trope not in compatible_tropes.get(t, []):
            print("what is new_trope", new_trope)
            print("what is compatible.get", compatible_tropes.get(t, []))
            return False
    return True"""

#allows the user to add, delete, or modify the order of the beats for each trope they selected
#might need to touch this up more
def edit_beats_for_trope(trope_name):
    data = trope_dict.get(trope_name, {})
    beats = data.get("beats", []).copy()
    if not beats:
        return []

    while True:
        print(f"\nCurrent beats for '{trope_name}':")
        for i, b in enumerate(beats, 1):
            print(f"{i}. {b}")

        print("\nOptions: [a]dd, [d]elete, [m]ove, [q]uit")
        choice = input("Choose an option: ").strip().lower()

        if choice == "a":
            new_beat = input("Enter new beat to add: ").strip()
            if new_beat:
                beats.append(new_beat)
        elif choice == "d":
            idx = int(input("Enter beat number to delete: ").strip()) - 1
            if 0 <= idx < len(beats):
                removed = beats.pop(idx)
                print(f"Removed: {removed}")
        elif choice == "m":
            idx = int(input("Enter beat number to move: ").strip()) - 1
            if 0 <= idx < len(beats):
                new_pos = int(input(f"Enter new position for beat {idx + 1}: ").strip()) - 1
                beat = beats.pop(idx)
                beats.insert(max(0, min(new_pos, len(beats))), beat)
        elif choice == "q":
            break
        else:
            print("Invalid option. Please choose again.")

    return beats

#wondering if re-ordering the example snippets versus lexical markers would make a difference
#creating the prompt used for model to generate the section
#might need to fix this
def build_section_prompt(previous_sections, current_trope, mc_name, li_name,
                         mc_pronouns, li_pronouns, dream_bible, spiciness=5, humor=5, angst=5, warmth=5,
                         snippets_per_trope=3, custom_beats=None):
    data = trope_dict.get(current_trope, {})
    #summary = data.get("core_conflict", "")
    beats = custom_beats if custom_beats is not None else data.get("beats", [])
    markers = data.get("lexical_markers", [])
    examples = snippet_db.get(current_trope, [])
    sampled_snippets = random.sample(examples, min(len(examples), snippets_per_trope)) if examples else []

    prompt = f"You are writing a New Adult romance story.\n"
    prompt += f"FIRST PERSON POV from {mc_name}.\n"
    prompt += f"Main Character: {mc_name} ({mc_pronouns['subj']}/{mc_pronouns['obj']}/{mc_pronouns['poss']})\n"
    prompt += f"Love Interest: {li_name} ({li_pronouns['subj']}/{li_pronouns['obj']}/{li_pronouns['poss']})\n\n"
    prompt += "RULES:\n- Never switch POV.\n- Keep character names and pronouns consistent.\n- Do not invent new romantic leads.\n\n"
    prompt += f"TONE: Spiciness={spiciness}/10, Humor={humor}/10, Angst={angst}/10, Warmth={warmth}/10\n\n"
    prompt += "Dream Love Interest Character Bible (use naturally, not overemphasized):\n"
    prompt += json.dumps(dream_bible, indent=2) + "\n\n"

    if previous_sections:
        prompt += "Story so far:\n" + "\n".join(previous_sections) + "\n\n"
        prompt += f"Continue the story using the trope '{current_trope}'.\n"
    else:
        prompt += f"Start a story using the trope '{current_trope}'.\n"

    if beats:
        prompt += "Suggested Beats (inspiration):\n" + "\n".join(f"- {b}" for b in beats) + "\n\n"

    if sampled_snippets:
        #print("what are sampled_snippets", sampled_snippets)
        prompt += "Example snippets (inspiration only — do NOT copy phrases; use only tone, pacing, and emotional texture):\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(sampled_snippets)) + "\n"

    if markers:
        prompt += "Lexical Markers (optional flavor, use sparingly; avoid repetition): " + ", ".join(markers) + "\n\n"

    """if markers:
        prompt += "Lexical Markers (optional flavor): " + ", ".join(markers) + "\n\n"

       if sampled_snippets:
        prompt += "Example snippets (inspiration only):\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(sampled_snippets)) + "\n"
    """
    prompt += "\nWrite 3–5 paragraphs using this trope naturally while maintaining continuity."
    return prompt

#might need to fix this
def generate_multi_trope_story(
    selected_tropes,
    protagonist_name,
    love_interest_name,
    mc_p,
    li_p,
    dream_bible,
    custom_beats,
    spiciness=5,
    humor=5,
    angst=5,
    warmth=5,
    snippets_per_trope=3,
    model="gpt-4.1",
    max_tokens=800,
    smooth=True
):

    sections = []

    # for trope in selected_tropes:
    #     prompt = build_section_prompt(
    #         sections,
    #         trope,
    #         protagonist_name,
    #         love_interest_name,
    #         mc_p,
    #         li_p,
    #         dream_bible,
    #         spiciness,
    #         humor,
    #         angst,
    #         warmth,
    #         snippets_per_trope,
    #         custom_beats.trope
    #     )

    for i in range(len(selected_tropes)):
        prompt = build_section_prompt(
            sections,
            selected_tropes[i],
            protagonist_name,
            love_interest_name,
            mc_p,
            li_p,
            dream_bible,
            spiciness,
            humor,
            angst,
            warmth,
            snippets_per_trope,
            custom_beats[i]["beats"]
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a creative, engaging New Adult romance writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.85,
        )

        section_text = response.choices[0].message.content.strip()
        sections.append(section_text)

    if smooth:
        smoothing_prompt = (
            f"The protagonist is {protagonist_name} ({mc_p['subj']}/{mc_p['obj']}/{mc_p['poss']}). "
            f"The love interest is {love_interest_name} ({li_p['subj']}/{li_p['obj']}/{li_p['poss']}).\n"
            "Keep POV strictly first-person and consistent.\n"
            f"TONE GUIDANCE: Spiciness={spiciness}/10, Humor={humor}/10, Angst={angst}/10, Warmth={warmth}/10\n"
            "Merge the following sections into a single coherent story:\n\n"
            + "\n\n".join(sections)
            + "\n\nSmooth transitions, fix any contradictions, and maintain character continuity."
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert romance story editor."},
                {"role": "user", "content": smoothing_prompt}
            ],
            max_tokens=max_tokens * 2,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    return "\n\n".join(sections)

######################################################################################################################
### Code to manually run the story generation with just python file execution
### Uncomment to use outside of FastAPI

#selected_tropes = ["Enemies to Lovers", "Grumpy and Sunshine", "Fake Relationship"]
#selected_tropes = ["Friends to Lovers", "Second Chance Romance", "Best Friend's Brother"]
#selected_tropes = ["Love Triangle", "Forbidden Love", "Secret Billionaire"]
#selected_tropes = ["Love Triangle"]
# selected_tropes = ["Enemies to Lovers", "Grumpy and Sunshine", "Friends to Lovers"]

# """dominant = selected_tropes[0]
# for trope in selected_tropes[1:]:
#     if not is_compatible([dominant], trope):
#         raise ValueError(f"'{trope}' is not compatible with '{dominant}'.")"""

# #new compatibility check just making sure friends to lovers and enemies to lovers together
# if "Friends to Lovers" in selected_tropes and "Enemies to Lovers":
#     raise ValueError(f" Friends to Lovers isn't compatible with Enemies to Lovers, choose again ")


# custom_beats_dict = {}
# for trope in selected_tropes:
#     custom_beats_dict[trope] = edit_beats_for_trope(trope)


# """final_story = play_story_interactive(
#     selected_tropes,
#     mc_name,
#     li_name,
#     mc_pronouns,
#     li_pronouns,
#     dream_bible,
#     spiciness,
#     humor,
#     angst,
#     warmth,
#     custom_beats_dict=custom_beats_dict
# )"""

# story = generate_multi_trope_story(
#     selected_tropes,
#     mc_name,
#     li_name,
#     mc_pronouns,
#     li_pronouns,
#     dream_bible,
#     spiciness,
#     humor,
#     angst,
#     warmth
# )

# print("\n\nFINAL STORY:\n")
# print(story)

######################################################################################################################
### FastAPI implementation starts here for the BYOB web app

#new compatibility check just making sure friends to lovers and enemies to lovers together
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    selected_tropes: List[str]
    mc_name: str
    li_name: str
    mc_pronouns: str
    li_pronouns: str
    dream_bible: Dict[str, str]
    spiciness: int
    humor: int
    angst: int
    warmth: int
    custom_beats: List[Dict[str, List[str]]]


@app.post("/generate_story")
def generate_story(request: StoryRequest):
    warning = []
    selected_tropes = request.selected_tropes
    final_story = ""

    if "Friends to Lovers" in selected_tropes and "Enemies to Lovers" in selected_tropes:
        warning.append(f" Friends to Lovers isn't compatible with Enemies to Lovers, choose again ")
    else:
        # For not not implemented
        custom_beats_dict = {} 

        mc_pronouns = PRONOUNS.get(request.mc_pronouns.lower(), PRONOUNS["female"])
        li_pronouns = PRONOUNS.get(request.li_pronouns.lower(), PRONOUNS["male"])

        final_story = generate_multi_trope_story(
            request.selected_tropes,
            request.mc_name,
            request.li_name,
            mc_pronouns,
            li_pronouns,
            request.dream_bible,
            request.custom_beats,
            request.spiciness,
            request.humor,
            request.angst,
            request.warmth
        )
        
    return {
        "story": final_story,
        "warnings": warning
    }

