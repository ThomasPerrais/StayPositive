from typing import List
import openai
from variables import DAYS, PROMPT, DEFAULT_LANG, SUMMARY_TYPES


def summarize_week(week_moments: List[List[str]], summary_type: str = SUMMARY_TYPES[DEFAULT_LANG][0], sep: chr = ';'):
    return __summarize_time_period(week_moments, DAYS[DEFAULT_LANG], summary_type, sep)


def __summarize_time_period(time_period_moments: List[List[str]], time_period_names: List[str],
                            summary_type: str, sep: chr):
    prompt = PROMPT[DEFAULT_LANG].format(summary_type)
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
