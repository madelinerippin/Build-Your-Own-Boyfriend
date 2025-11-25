#ok this is the best one with decisions and full story output and also allowed
#the beat modification which is good

import json
import random
import openai
from openai import OpenAI

#dictionary to get main character and love interest's pronouns after user input
PRONOUNS = {
    "male": {"subj": "he", "obj": "him", "poss": "his"},
    "female": {"subj": "she", "obj": "her", "poss": "her"},
    "nonbinary": {"subj": "they", "obj": "them", "poss": "their"}
}

#dictionary to ensure the user doesn't do friends to lovers and enemies to lovers in the same generation
#this can be fixed because there can be a lot more combos than what this is allowing
compatible_tropes = {
    "Enemies to Lovers": ["Grumpy and Sunshine", "Fake Relationship", "Forbidden Love"],
    "Friends to Lovers": ["Second Chance Romance", "Best Friend’s Brother"],
    "Forbidden Love": ["Love Triangle", "Secret Billionaire", "Enemies to Lovers"],
    "Fake Relationship": ["Grumpy and Sunshine", "Enemies to Lovers", "Secret Billionaire"],
    "Grumpy and Sunshine": ["Fake Relationship", "Enemies to Lovers", "Age Gap"],
    "Love Triangle": ["Forbidden Love", "Secret Billionaire"],
    "Best Friend’s Brother": ["Friends to Lovers", "Second Chance Romance"],
    "Second Chance Romance": ["Friends to Lovers", "Best Friend’s Brother"],
    "Age Gap": ["Grumpy and Sunshine", "Secret Billionaire"],
    "Secret Billionaire": ["Forbidden Love", "Fake Relationship", "Age Gap", "Love Triangle"]
}


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
client = OpenAI(api_key="")

#all of the user input sections!! There are default options right now if the user doesn't fill something out
#but should change that to make required sections say "please enter a valid name", etc

#the user's name and gender (thinking this can be the first page)
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

#checks if the tropes the user selected are compatible with each other
#currently don't have a limit on the number of tropes the user selects so long as they're compatible
#idk if we should have that tho?
def is_compatible(selected_tropes, new_trope):
    for t in selected_tropes:
        if new_trope not in compatible_tropes.get(t, []):
            return False
    return True

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
        print("what are sampled_snippets", sampled_snippets)
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
def play_story_interactive(selected_tropes, mc_name, li_name, mc_pronouns, li_pronouns, dream_bible,
                           spiciness=5, humor=5, angst=5, warmth=5, snippets_per_trope=3, model="gpt-4.1",
                           max_tokens=800, custom_beats_dict=None):
    story_so_far = []

    for trope in selected_tropes:
        custom_beats = custom_beats_dict.get(trope) if custom_beats_dict else None
        prompt = build_section_prompt(
            story_so_far,
            trope,
            mc_name,
            li_name,
            mc_pronouns,
            li_pronouns,
            dream_bible,
            spiciness,
            humor,
            angst,
            warmth,
            snippets_per_trope,
            custom_beats
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

        story_chunk = response.choices[0].message.content.strip()
        print("\n" + story_chunk)
        story_so_far.append(story_chunk)

        #does the branching decision based on what the model has generated thus far
        branch_prompt = (
            f"Based on the story above, generate 3 natural, context-sensitive choices "
            f"the protagonist could take next. Maintain POV, tone, and character.\n\n"
            f"Story so far:\n{story_chunk}\n\n"
            "Output as: A) ..., B) ..., C) ..."
        )

        branch_resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in interactive romance storytelling."},
                {"role": "user", "content": branch_prompt}
            ],
            max_tokens=300,
            temperature=0.8,
        )

        choices_text = branch_resp.choices[0].message.content.strip()
        print("\nMAKE YOUR CHOICE")
        print(choices_text)

        #separate choices
        choices_lines = [line.strip() for line in choices_text.split("\n") if line.strip()]
        valid_choices = {}
        for line in choices_lines:
            if ")" in line:
                key, desc = line.split(")", 1)
                key = key.strip().upper()
                valid_choices[key] = desc.strip()

        user_choice = input(f"Choose ({'/'.join(valid_choices.keys())}): ").strip().upper()
        if user_choice not in valid_choices:
            user_choice = list(valid_choices.keys())[0]
        #print(f"\nUser choice applied: {user_choice}) {valid_choices[user_choice]}")

        #once the user decides prompt based off of that decision
        """resolve_prompt = (
            f"Continue the story from the previous section, incorporating the user's choice:\n"
            f"{story_chunk}\n\n"
            f"User choice: {valid_choices[user_choice]}\n\n"
            "Write 3–5 paragraphs smoothly, respecting character, POV, tone, and continuity."
        )"""

        resolve_prompt = (
            f"Continue the story from the previous section, incorporating the user's choice:\n"
            f"{story_chunk}\n\n"
            f"User choice: {valid_choices[user_choice]}\n\n"
            "Write 1–2 sentences that smoothly resolve the immediate choice, setting up the next story beat. "
            "Do NOT write a full paragraph. Do NOT advance the plot more than necessary."
        )

        resolve_resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a creative, engaging New Adult romance writer."},
                {"role": "user", "content": resolve_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.85,
        )

        resolved_chunk = resolve_resp.choices[0].message.content.strip()
        print("\n" + resolved_chunk)
        story_so_far.append(resolved_chunk)

    print("\n\n THE END! THANKS FOR PLAYING! \n")
    return "\n\n".join(story_so_far)

######################################################################################################################

selected_tropes = ["Enemies to Lovers", "Grumpy and Sunshine", "Fake Relationship"]

dominant = selected_tropes[0]
for trope in selected_tropes[1:]:
    if not is_compatible([dominant], trope):
        raise ValueError(f"'{trope}' is not compatible with '{dominant}'.")


custom_beats_dict = {}
for trope in selected_tropes:
    custom_beats_dict[trope] = edit_beats_for_trope(trope)


final_story = play_story_interactive(
    selected_tropes,
    mc_name,
    li_name,
    mc_pronouns,
    li_pronouns,
    dream_bible,
    spiciness,
    humor,
    angst,
    warmth,
    custom_beats_dict=custom_beats_dict
)
