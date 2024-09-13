# This is the server

from collections import defaultdict
from concurrent import futures

import grpc

import questions_pb2_grpc
from questions_pb2 import (Question, QuestionByIdResponse,
                           QuestionDeleteResponse, QuestionEditingResponse,
                           QuestionPostingResponse, QuestionResponse)

# Now you have to write questions exactly as they may
# look in the database - same as the specified in .proto
# message Question {
#    int32 question_id = 1;
#    string category = 2;
#    string difficulty_level =3;
#    bool is_MCQ =4;
#    float grade =5;
# }

questions_hypothetically_in_the_database = [
	Question(question_id=1, category="programming languages", difficulty_level="easy", is_MCQ=True, grade = 5),
	Question(question_id=2, category="UML diagrams", difficulty_level="easy", is_MCQ=True, grade = 5),
	Question(question_id=3, category="programming languages", difficulty_level="moderate", is_MCQ=False, grade = 5),
	Question(question_id=4, category="UML diagrams", difficulty_level="moderate", is_MCQ=False, grade = 5),
	Question(question_id=5, category="Embedded systems", difficulty_level="difficult", is_MCQ=True, grade = 5),
]

# class containing all services to be offered by this microservice

# the class Question Service inherits from ...Servicer
class QuestionService(questions_pb2_grpc.QuestionsServicer):
# Arguments must be non-positional
	def GetAllQuestions(self, request, context):
		if not request: context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")
		return QuestionResponse(questions=questions_hypothetically_in_the_database)
        
# Arguments to this function must be non-positional
	def GetQuestionById(self, request, context):
		if not request: context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")
		dd = defaultdict(Question)
		for q in questions_hypothetically_in_the_database:
			dd[q.question_id]=q
		return QuestionByIdResponse(question=dd[request.question_id])
	
# Arguments to this function must be non-positional
	def PostQuestion(self, request, context):
		if not request: context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")
		questions_hypothetically_in_the_database.append(request.question)
		print(questions_hypothetically_in_the_database)
		return QuestionPostingResponse(posting_message="Question posted in database")
	
# Arguments to this function must be non-positional
	def ModifyQuestion(self, request, context):
		if not request: context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")
		dd = defaultdict(Question)
		for q in questions_hypothetically_in_the_database:
			dd[q.question_id]=q
		if request.question_id in dd.keys():
			# update question and return success msg
			dd[request.question_id].grade= request.grade
			print(questions_hypothetically_in_the_database)
			return QuestionEditingResponse(update_message="Question updated in database")
		else:
			print("Question Id not found")
			context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")

# Arguments to this function must be non-positional
	def DeleteQuestion(self, request, context):
		if not request: context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")
		dd = defaultdict(Question)
		for q in questions_hypothetically_in_the_database:
			dd[q.question_id]=q
		if request.question_id in dd.keys():
			# delete question and return success msg
			del dd[request.question_id]
			print(questions_hypothetically_in_the_database)
			return QuestionEditingResponse(update_message="Question deleted from database")
		else:
			print("Question Id not found")
			context.abort(grpc.StatusCode.NOT_FOUND, "Request not found")


# running the server
def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	questions_pb2_grpc.add_QuestionsServicer_to_server(QuestionService(), server)
	server.add_insecure_port("[::]:50051")
	server.start()
	server.wait_for_termination()

if __name__ == "__main__":
    serve()