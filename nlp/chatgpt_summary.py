from typing import List
import openai

days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

size = 50

base_prompt = "Peux-tu résumer en {} maximum ma semaine à partir des petits bonheurs que j'ai noté chaque jour de la semaine."

# prompts = [
#     # "{0} a écrit 3 petits bonheurs qui lui sont arrivés chaque jour de la semaine et qui sont retranscrit ci-dessous. Résume la semaine de {0} en moins de {1} mots.",
#     # "J'ai écrit 3 petits bonheurs qui me sont arrivés chaque jour de la semaine et qui sont retranscrit ci-dessous. Résume ma semaine en moins de {} mots.".format(size),
#     # "Résume en moins de {1} mots ma semaine à partir des 3 petits bonheurs de chacune de mes journées listés ci-dessous",
#     "Peux-tu résumer en moins de 50 mots ma semaine à partir des 3 petits bonheurs que j'ai noté chaque jour de la semaine.",
#     "Peux-tu résumer en 5 adjectifs maximum ma semaine à partir des 3 petits bonheurs que j'ai noté chaque jour de la semaine.",
#     "Peux-tu résumer en une phrase ma semaine à partir des 3 petits bonheurs que j'ai noté chaque jour de la semaine.",
# ]


def summarize_week(week_moments: List[List[str]], summary_type: str = "50 mots", sep: chr = ';'):
    return __summarize_time_period(week_moments, days, summary_type, sep)


def __summarize_time_period(time_period_moments: List[List[str]], time_period_names: List[str],
                            summary_type: str, sep: chr):
    prompt = base_prompt.format(summary_type)
    for m_name, moments in zip(time_period_names, time_period_moments):
        if len(moments) != 0:
            prompt += " " + __format_moments(m_name, moments, sep)
    try:
        res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content": prompt}])
        return res["choices"][0]["message"]["content"]
    except:
        return "[ERROR] - call to ChatGPT failed..."



def __format_moments(m_name: str, moments: List[str], sep: chr = ';'):
    return m_name + ": " + "{} ".format(sep).join(moments) + "."
