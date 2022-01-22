from attendance.models import Lab_Attendance
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
from InternalMarksPrediction.models import TotalMarks
from Accounts.models import Account
from student.models import Student


def algorithm(request):

    df = pd.read_csv('dataset/student_performance_reports.csv')
    head = df.head()
    independent = df.drop('Performance', axis='columns')
    target = df['Performance']
    model = tree.DecisionTreeClassifier(
        max_leaf_nodes=10, random_state=10, criterion='gini') 
    model.fit(independent, target)
    score = model.score(independent, target)

    # DATABSE QUERY
    account = Student.objects.get(user_id=request.user.id)
    total_marks = TotalMarks.objects.get(user_id=account.id)
    attendance = total_marks.total_attendance_marks
    lab_attendance = total_marks.total_lab_attendance_marks
    assignment = total_marks.total_assignment_marks
    lab_assignment = total_marks.total_lab_assignment_marks
    class_assesment = total_marks.total_class_assesment_marks
    mid_assessment = total_marks.total_mid_assessment_marks
    final_assessment = total_marks.total_final_assessment_marks


    if attendance == 0 and lab_attendance == 0 and lab_assignment == 0 and assignment == 0:
        return 'N/A'
    
    predict = model.predict([[attendance, lab_attendance, assignment,
                            lab_assignment, class_assesment, mid_assessment, final_assessment]])
    predicts = str(predict)
    if predict == 0:
        predict = "Bad"
    elif predict == 1:
        predict = 'Average'

    elif predict == 2:
        predict = "Good"

    return predict
