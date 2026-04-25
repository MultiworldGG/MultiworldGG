from .types import TriviaQuestion, Topic

def format_dkc2_question(question: list[str]) -> list[str]:
    total_lines = len(question)
    if total_lines == 1:
        question.insert(0, "°")
        question.insert(0, "°")
        question.append("°")
        question.append("°")
        question.append("°")
    elif total_lines == 2:
        question.insert(0, "°")
        question.insert(0, "°")
        question.append("°")
        question.append("°")
    elif total_lines == 3:
        question.insert(0, "°")
        question.append("°")
        question.append("°")
    elif total_lines == 4:
        question.insert(0, "°")
        question.append("°")
    elif total_lines == 5:
        question.append("°")
    return question


def format_dkc2_answer(answer: str) -> str:
    if "°" in answer:
        answer = answer.split("°")
        return f"{answer[0].strip()}°        {answer[1].strip()}°"
    else:
        return answer.strip() + "°°"


def parser_version_1(topic_data: list[str], valid_topics: list[str], is_dkc2: bool) -> Topic | None:
    if "GAME:" not in topic_data[1]:
        print (f"Failed to fetch the game name.")
        return None
    topic_name = topic_data[1][5:].strip()
    if len(valid_topics) != 0:
        if topic_name not in valid_topics:
            return None
    if "AUTHOR:" not in topic_data[2]:
        print (f"Failed to fetch the trivia author.")
        return None
    topic_author = topic_data[2][7:].strip()
    if "---" not in topic_data[3]:
        print (f"Failed to find a separator between the header and the first question.")
        return None

    idx = 4
    trivia_easy = []
    trivia_medium = []
    trivia_hard = []
    processed_question = False
    processed_answers = False
    while idx < len(topic_data):
        if "---" in topic_data[idx]:
            if not processed_question or not processed_answers:
                print (f"[{topic_name} | {topic_author}] A question had invalid format before line {idx+1}.")
                return None
            idx += 1
            processed_question = False
            processed_answers = False
        elif "QUESTION:" in topic_data[idx]:
            difficulty = topic_data[idx].split(": ")[1].rstrip()
            if difficulty not in ["EASY", "MEDIUM", "HARD"]:
                print (f"[{topic_name} | {topic_author}] Unknown difficulty detected at line {idx+1}.")
                return None
            idx += 1
            question = []
            for idy in range(7):
                line = topic_data[idx+idy].strip()
                if len(line) > 32:
                    print (f"[{topic_name} | {topic_author}] Line {idx+1} exceeded the maximum allowed length of 32 (it has {len(line)}).")
                    return None
                # End of question
                if "ANSWERS:" in line:
                    break
                if is_dkc2:
                    question.append(f"{line.center(32, ' ').rstrip()}°")
                else:
                    question.append(f"{line.rstrip()}")
            else:
                print (f"[{topic_name} | {topic_author}] A question exceeded the max amount of allowed lines at line {idx+idy+1}.")
                return None
            idx += idy
            if is_dkc2:
                question = format_dkc2_question(question)
            else:
                question = " ".join(question)

            processed_question = True

        elif "ANSWERS:" in topic_data[idx]:
            idx += 1
            answers = []
            if is_dkc2:
                for idy in range(3):
                    answer = topic_data[idx+idy].strip()
                    if "°" in answer:
                        if len(answer.split("°")[0]) > 24 or len(answer.split("°")[1].strip()) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 for one of its lines (it has {len(answer)}).")
                            return None
                    else:
                        if len(answer) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 (it has {len(answer)}).")
                            return None
                    answers.append(format_dkc2_answer(answer))
            else:
                for idy in range(3):
                    answer = topic_data[idx+idy].strip()
                    if "°" in answer:
                        if len(answer.split("°")[0]) > 24 or len(answer.split("°")[1].strip()) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 for one of its lines (it has {len(answer)}).")
                            return None
                        answer = f"{answer.split("°")[0]} {answer.split("°")[1].strip()}"
                    else:
                        if len(answer) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 (it has {len(answer)}).")
                            return None
                    answers.append(answer)
            
            idx += 3
            question_data = TriviaQuestion(question=question, 
                                           topic_name=topic_name,
                                           author=topic_author,
                                           correct_answer=answers[0], 
                                           incorrect_answer_1=answers[1], 
                                           incorrect_answer_2=answers[2]
                                           )

            if difficulty == "EASY":
                trivia_easy.append(question_data)
            elif difficulty == "MEDIUM":
                trivia_medium.append(question_data)
            elif difficulty == "HARD":
                trivia_hard.append(question_data)

            processed_answers = True

        else:
            print (f"[{topic_name} | {topic_author}] Found an issue while parsing line {idx+1}:\n{topic_data[idx]}")
            return None

    return Topic(topic_name, trivia_easy, trivia_medium, trivia_hard)


def parser_version_2(topic_data: list[str], valid_topics: list[str], is_dkc2: bool) -> Topic | None:
    if "GAME:" not in topic_data[1]:
        print (f"Failed to fetch the game name.")
        return None
    topic_name = topic_data[1][5:].strip()
    if len(valid_topics) != 0:
        if topic_name not in valid_topics:
            return None
    if "AUTHOR:" not in topic_data[2]:
        print (f"Failed to fetch the trivia author.")
        return None
    topic_author = topic_data[2][7:].strip()
    if "---" not in topic_data[3]:
        print (f"Failed to find a separator between the header and the first question.")
        return None
    
    idx = 4
    trivia_easy = []
    trivia_medium = []
    trivia_hard = []
    processed_question = False
    processed_answers = False
    while idx < len(topic_data):
        if "---" in topic_data[idx]:
            if not processed_question or not processed_answers:
                print (f"[{topic_name} | {topic_author}] A question had invalid format before line {idx+1}.")
                return None
            idx += 1
            processed_question = False
            processed_answers = False
        elif "QUESTION:" in topic_data[idx]:
            difficulty = topic_data[idx].split(": ")[1].rstrip()
            if difficulty not in ["EASY", "MEDIUM", "HARD"]:
                print (f"[{topic_name} | {topic_author}] Unknown difficulty detected at line {idx+1}.")
                return None
            idx += 1
            question = []
            for idy in range(7):
                line = topic_data[idx+idy].strip()
                if len(line) > 32:
                    print (f"[{topic_name} | {topic_author}] Line {idx+1} exceeded the maximum allowed length of 32 (it has {len(line)}).")
                    return None
                # End of question
                if "ANSWERS:" in line:
                    break
                if is_dkc2:
                    question.append(f"{line.center(32, ' ').rstrip()}°")
                else:
                    question.append(f"{line.rstrip()}")
            else:
                print (f"[{topic_name} | {topic_author}] A question exceeded the max amount of allowed lines at line {idx+idy+1}.")
                return None
            idx += idy
            if is_dkc2:
                question = format_dkc2_question(question)
            else:
                question = " ".join(question)

            processed_question = True

        elif "ANSWERS:" in topic_data[idx]:
            idx += 1
            answers = []
            if is_dkc2:
                for idy in range(4):
                    answer = topic_data[idx+idy].strip()
                    if "°" in answer:
                        if len(answer.split("°")[0]) > 24 or len(answer.split("°")[1].strip()) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 for one of its lines (it has {len(answer)}).")
                            return None
                    else:
                        if len(answer) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 (it has {len(answer)}).")
                            return None
                    answers.append(format_dkc2_answer(answer))
            else:
                for idy in range(4):
                    answer = topic_data[idx+idy].strip()
                    if "°" in answer:
                        if len(answer.split("°")[0]) > 24 or len(answer.split("°")[1].strip()) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 for one of its lines (it has {len(answer)}).")
                            return None
                        answer = f"{answer.split("°")[0]} {answer.split("°")[1].strip()}"
                    else:
                        if len(answer) > 24:
                            print (f"[{topic_name} | {topic_author}] Line {idx+idy+1} exceeded the maximum allowed length of 24 (it has {len(answer)}).")
                            return None
                    answers.append(answer)
            
            idx += 4
            question_data = TriviaQuestion(question=question, 
                                           topic_name=topic_name,
                                           author=topic_author,
                                           correct_answer=answers[0], 
                                           incorrect_answer_1=answers[1], 
                                           incorrect_answer_2=answers[2], 
                                           incorrect_answer_3=answers[3]
                                           )

            if difficulty == "EASY":
                trivia_easy.append(question_data)
            elif difficulty == "MEDIUM":
                trivia_medium.append(question_data)
            elif difficulty == "HARD":
                trivia_hard.append(question_data)

            processed_answers = True

        else:
            print (f"[{topic_name} | {topic_author}] Found an issue while parsing line {idx+1}:\n{topic_data[idx]}")
            return None

    return Topic(topic_name, trivia_easy, trivia_medium, trivia_hard)
