# This is not a necessary file in the application
# We are using this only to try the files containing the prtocol buffer files
# Protocol Buffer files will eventually formulate the service server

import grpc

from questions_pb2 import (Question, QuestionByIdRequest,
                           QuestionDeleteRequest, QuestionEditingRequest,
                           QuestionPostingRequest, QuestionRequest)
from questions_pb2_grpc import QuestionsStub


def main():
	print("Hello ")

	channel = grpc.insecure_channel("localhost:50051")
	client = QuestionsStub(channel)

	# Consuming the rpc named GetAllQuestions
	# request = QuestionRequest()
	# print(client.GetAllQuestions(request))

	# Consuming the rpc named GetQuestionById
	# request = QuestionByIdRequest(question_id=2)
	# print(client.GetQuestionById(request))

	# Consuming the rpc named PostQuestion
	# question_to_be_posted=Question(question_id=40, category="Soft skills", difficulty_level="moderate", is_MCQ=False, grade=3)
	# request = QuestionPostingRequest(question=question_to_be_posted)
	# print(client.PostQuestion(request))

	# Consuming the rpc named ModifyQuestion
	question_id_to_be_updated = 2
	new_grade = 4.78
	request = QuestionEditingRequest(question_id=question_id_to_be_updated, grade=new_grade)
	client.ModifyQuestion(request)
    

	# Consuming the rpc named DeleteQuestion
	# question_id_to_be_deleted = 1
	# request = QuestionDeleteRequest(question_id=question_id_to_be_deleted)
	# print(client.DeleteQuestion(request))


if __name__ == '__main__':
    main()