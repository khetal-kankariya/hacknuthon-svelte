class questionsSchema:
    def __init__(self, job_post, questions):
        self.job_post = job_post
        self.questions = questions
        
    def to_dict(self):
        return {'job_post': self.job_post, 'questions': [str(q) for q in self.questions]}

    @staticmethod
    def from_dict(data):
        return questionsSchema(data['job_post'], data['questions'])