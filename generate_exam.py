import argparse
import json
import xlsxwriter
from os.path import exists, basename
from sys import version_info
from random import sample, shuffle

global TIMELIMIT
TIMELIMIT = 60 # 60 second time limit for kahoot

if not ((version_info.major >= 3) and (version_info.minor >= 9)):
    print(basename(__file__) + ": error: this script requires at least Python 3.9")
    exit(9)

def main():
    parser = argparse.ArgumentParser(description='Converts NCVEC Amateur Radio question pools into JSON files.')
    parser.add_argument("-i", "--input", help="Filename of question pool to be inported", required=True)
    parser.add_argument("-o", "--output", help="Directs the JSON to a name of your choice", required=True)
    parser.add_argument("-c", "--class", help="Dictate exam class (i.e. Technician, General, Amateur Extra)", choices=['T', 'G', 'AE'], dest='licenseclass', required=True)
    parser.add_argument('-k', "--kahoot", help="Export to .xlsx to import into Kahoot!", action='store_true')
    args = parser.parse_args()

    if not exists(args.input):
        print(basename(__file__) + ": error: the input file does not exist")
        exit(0)

    file = open(str(args.input), "r", encoding="utf-8")
    pool_json = file.read()
    file.close()
    pool_dict = json.loads(pool_json)
    exam = exam_generator(args, pool_dict)
    if args.kahoot:
        createxlsx(exam, args)
    else:
        with open(str(args.output), 'w', encoding='utf-8') as filename:
            json.dump(exam, filename, ensure_ascii=False, indent=4)

    
def sort_by_section(pool_dict):
    sorted = [[] for i in range(10)] # create list of 10 empty lists
    for question in pool_dict:
        #print(question['id'][1])
        sorted[int(question['id'][1])].append(question)
    return sorted

def exam_generator(args, pool):
    if args.licenseclass == 'T':
        breakdown = [3, 6, 3, 3, 2, 4, 4, 4, 4, 2] # Section 10 is indice [0]
    elif args.licenseclass == 'G':
        breakdown = [2, 5, 5, 3, 5, 3, 2, 3, 3, 4]
    elif args.licenseclass == 'AE':
        breakdown = [1, 6, 5, 3, 5, 4, 6, 8, 4, 8]
    else:
        print(basename(__file__) + ": error: could not parse license class")

    exam = []
    i = 0

    if args.kahoot:
        pool = shortenexam(pool)
    
    pool = sort_by_section(pool)

    for section in pool:
        q_random_nums = sample(range(len(section)), breakdown[i])
        for qnum in q_random_nums:
            exam.append(section[qnum])
        i += 1

    shuffle(exam)
    return exam

def createxlsx(exam, args):
    workbook = xlsxwriter.Workbook(f'{args.output}.xlsx')
    worksheet = workbook.add_worksheet()
    # write kahoot template headers (they check for these for some reason)
    worksheet.write('B8', 'Question - max 95 characters')
    worksheet.write('C8', 'Answer 1 - max 60 characters')
    worksheet.write('D8', 'Answer 2 - max 60 characters')
    worksheet.write('E8', 'Answer 3 - max 60 characters')
    worksheet.write('F8', 'Answer 4 - max 60 characters')
    worksheet.write('G8', 'Time limit (sec) - 5,10,20,30,60,90 or 120 secs')
    worksheet.write('H8', 'Correct answer(s) - choose at least one')
    for question in range(35):
        worksheet.write('B' + str(9 + int(question)), exam[question]["question"])
        worksheet.write('C' + str(9 + int(question)), exam[question]["answers"][0])
        worksheet.write('D' + str(9 + int(question)), exam[question]["answers"][1])
        worksheet.write('E' + str(9 + int(question)), exam[question]["answers"][2])
        worksheet.write('F' + str(9 + int(question)), exam[question]["answers"][3])
        worksheet.write('G' + str(9 + int(question)), TIMELIMIT)
        worksheet.write('H' + str(9 + int(question)), int(exam[question]["correct"]) + 1)
    workbook.close()

def shortenexam(questionList):
    MAX_QUESTION_LENGTH = 95
    MAX_ANSWER_LENGTH = 60
    short_pool = []
    for question in questionList:
        if len(question["question"]) > MAX_QUESTION_LENGTH:
            continue
        for answer in question["answers"]:
            if len(answer) > MAX_ANSWER_LENGTH:
                break
        else:
            short_pool.append(question)
    return short_pool

if __name__ == "__main__":
    main()


        
