from rest_framework import serializers
from .models import StudentCourse
from accounts.models import Account
from courses.models import Course
from accounts.serializers import AccountSerializer
from contents.models import Content
from contents.serializers import ContentSerializer


class StudentCourseSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    student_email = serializers.CharField(source="student.email")
    student_id = serializers.CharField(source="student.id", read_only=True)

    class Meta:
        model = StudentCourse
        fields = [
            "id", "student_id", "student_username", "student_email", "status"]
        

class CourseStudentsSerializer(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True)
    
    class Meta:
        model = Course
        fields = [
            "id", "name", "students_courses"]
        extra_kwargs = {
            "name": {
                "read_only": True
            }
        }

    def update(self, instance, validated_data):
        studentsNotfound = []
        studentsUser = []
        for student in validated_data["students_courses"]:
            courseStudent = student["student"]
            user = Account.objects.filter(email=courseStudent["email"]).first()
            if user:
                studentsUser.append(user)
            else:
                studentsNotfound.append(courseStudent["email"])

        if studentsNotfound:
            # divide uma string por uma lista
            stringMail = ", ".join(studentsNotfound)
            raise serializers.ValidationError({"detail": f"No active accounts was found: {stringMail}."})

        if not self.partial:
            instance.students.add(*studentsUser)   
            return instance
        return super().update(instance, validated_data)    
        