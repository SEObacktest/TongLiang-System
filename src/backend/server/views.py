import io, os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from django.core.serializers import serialize
from django.http import FileResponse
from django.contrib.auth import login, logout, authenticate
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import xlwt

from .models import EvaluationUser, Activity, ActivityImage, UserImage, Interview, CurriculumVitae, Settlement

#hr每面试一个人得到的报酬，可以改
salaryrate = 100

# 参考: https://blog.csdn.net/weixin_55638841/article/details/133996079
def generate_excel(activity_list):

    # 2.创建一个工作簿(workbook)，并设置编码
    # Create a workbook and set encoding
    workbook = xlwt.Workbook(encoding='utf-8')

    # 3.创建一个工作表(worksheet)
    # Create a worksheet
    worksheet = workbook.add_sheet("党员活动信息")

    # 3.1 设置列宽
    # Set column width
    worksheet.col(0).width = 256 * 8  # 8个字符0的宽度
    worksheet.col(1).width = 256 * 12
    worksheet.col(2).width = 256 * 30
    worksheet.col(3).width = 256 * 30
    worksheet.col(4).width = 256 * 30
    worksheet.col(5).width = 256 * 20
    worksheet.col(6).width = 256 * 16

    # 3.2 设置表头行高
    # Set the height of the header row
    style = xlwt.easyxf('font:height 360;')
    row = worksheet.row(0)
    row.set_style(style)

    # 4.写表头部分
    # Write the header part
    # 4.1 表头数据
    # Header data
    header_list = ['活动ID', '活动名称', '负责党员', '开始时间', '结束时间', '地点', '心得', '活动类型', '是否通过', '是否审核', '审核人', '活动提交时间']

    # 4.2 写表头
    # Write the header
    for header_data in enumerate(header_list):
        worksheet.write(0, header_data[0], header_data[1], style)

    # 4.3 写表格内容数据
    # Write the table content data
    for index, row_data in enumerate(activity_list): # 遍历所有的活动取数据。 for each activity, get the data
        worksheet.write(index + 1, 0, row_data.id)  # 第一行为表头
        worksheet.write(index + 1, 1, row_data.name)
        worksheet.write(index + 1, 2, row_data.student.username)
        worksheet.write(index + 1, 3, row_data.startTime.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(index + 1, 4, row_data.endTime.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(index + 1, 5, row_data.location)
        worksheet.write(index + 1, 6, row_data.description)
        worksheet.write(index + 1, 7, row_data.type)
        worksheet.write(index + 1, 8, row_data.passed)
        worksheet.write(index + 1, 9, row_data.certified)
        if row_data.admin is not None:
            worksheet.write(index + 1, 10, row_data.admin.username)
        worksheet.write(index + 1, 11, row_data.registerTime.strftime('%Y-%m-%d %H:%M:%S'))

        # 表头行高
        row = worksheet.row(index + 1)
        row.set_style(style)

    # 生成文件名称，名称包含法规导出 + 年月日时分秒数字的组合，避免重复
    # Generate the file name, the name contains the combination of the export of laws and regulations + the combination of year, month, day, hour, minute, and second numbers to avoid duplication
    file_name = '党员活动信息导出{}'.format(datetime.now().strftime(format('%Y-%m-%d %H:%M:%S')))

    # 5.保存文件
    # Save the file

    # 5.1 保存到本地文件：保存文件目录级别在项目目录下，与apps同级
    # Save to local file: save the file directory level under the project directory, at the same level as apps
    workbook.save("media/files/last.xls")

    # 5.2 保存文件流到内存
    # Save the file stream to memory
    sio = io.BytesIO()
    workbook.save(sio)
    sio.seek(0)

    # 5.3 返回数据给前端
    # Return data to the front end

    # 5.3.1 获取文件流，设置文件类型
    # Get the file stream and set the file type
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')

    # 5.3.2 配置Response Headers中`Content-Disposition`信息，支持中文
    # Configure the `Content-Disposition` information in the Response Headers to support Chinese
    response['Content-Disposition'] = "attachment;filename={}.xls".format(escape_uri_path(file_name))

    # 5.3.3 必须将`Content-Disposition`暴露给前端，否则前端获取不到信息
    # `Content-Disposition` must be exposed to the front end, otherwise the front end cannot obtain the information
    response['Access-Control-Expose-Headers'] = "Content-Disposition"

    # 5.3.4 返回数据给前端
    response.write(sio.getvalue())

    print("用户导出excel成功")

    return response


class Server(viewsets.GenericViewSet):

    @action(detail=False, methods=['get'])
    def get_token(self, request, *args, **kwargs):
        # print("用户请求了csrf_token")
        csrf_token = get_token(request)
        resp = {
            'status': True,
            'data': csrf_token
        }
        print("用户成功获取csrf_token值：" + csrf_token)
        return Response(resp)

    #  登录
    #################################################

    @action(detail=False, methods=['get'])
    def is_login(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.isAdmin:
                resp = {
                    'status': True,
                    'data': {
                        'userId': request.user.userId,
                        'username': request.user.username,
                        'phone': request.user.phone,
                        'is_admin': True
                    },
                    'message': '已经登录了'
                }
            else:
                resp = {
                    'status': True,
                    'data': {
                        'userId': request.user.userId,
                        'username': request.user.username,
                        'phone': request.user.phone,
                        'bankCard': request.user.bankCard,
                        'bank': request.user.bank,
                        'accountHolderName': request.user.accountHolderName,
                        'city': request.user.city,
                        'age': request.user.age,
                        'gender': request.user.gender,
                        'is_admin': False
                    },
                    'message': '已经登录了'
                }
                print("用户已经登录了")
        else:
            resp = {
                'status': False,
                'message': '还没有登录'
            }
            print("用户还没有登录")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def admin_login(self, request, *args, **kwargs):
        print("管理员请求了登录")
        # data = json.loads(request.body)
        data = request.data
        userId = data['adminId']
        password = data['password']
        try:
            user = EvaluationUser.objects.get(userId=userId)
            if user.check_password(password):
                if not user.isAdmin:
                    resp = {
                        'status': False,
                        'message': '非管理员'
                    }
                    print("管理员登录失败，非管理员")
                    return Response(resp)
                login(request, user)
                resp = {
                    'status': True,
                    'message': '登录成功'
                }
                print("管理员登录成功")
            else:
                resp = {
                    'status': False,
                    'message': '密码错误'
                }
                print("管理员登录失败，密码错误")
        except:
            resp = {
                'status': False,
                'message': '管理员不存在'
            }
            print("管理员登录失败，管理员不存在")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def student_login(self, request, *args, **kwargs):
        print("用户请求了登录")
        data = request.data
        userId = data['userId']
        password = data['password']
        try:
            user = EvaluationUser.objects.get(userId=userId)
            if user.check_password(password):
                login(request, user)
                resp = {
                    'status': True,
                    'data': {
                        'studentId': user.userId,
                        'username': user.username,
                        'phone': user.phone,
                        'account': user.account,
                        'bankCard': user.bankCard,
                        'bank': user.bank,
                        'accountHolderName': user.accountHolderName,
                        'idCard': user.idCard,
                        'age': user.age,
                        'gender': user.gender,
                        'last_login': user.last_login,
                        'date_joined': user.date_joined,
                        'isAdmin': user.isAdmin,
                    },
                    'message': '登录成功',
                }
                print(user.userId + "用户登录成功")
                # return Response(resp).set_cookie("studentId", student.studentId, max_age=3600 * 24 * 1)
            else:
                resp = {
                    'status': False,
                    'message': '密码错误',
                }
                print("用户登录失败，密码错误")
        except:
            resp = {
                'status': False,
                'message': '用户不存在'
            }
            print("用户登录失败，用户不存在")
        return Response(resp)

    @action(detail=False, methods=['get'])
    def logout(self, request, *args, **kwargs):
        print("用户请求了登出")
        logout(request)
        resp = {
            'status': True,
            'message': '用户登出成功'
        }
        print("用户登出成功")
        return Response(resp)

    # 注册
    #################################################

    @action(detail=False, methods=['post'])
    def admin_register(self, request, *args, **kwargs):
        print("管理员请求了注册")
        # data = json.loads(request.body)
        data = request.data
        userId = data['adminId']
        username = data['username']
        password = data['password']
        phone = data['phone']
        try:
            admin = EvaluationUser.objects.create_user(userId=userId, username=username, phone=phone, password=password,
                                                       isAdmin=True)
            admin.save()
            resp = {
                'status': True,
                'message': '注册成功'
            }
            print("管理员注册成功")

        except:
            resp = {
                'status': False,
                'message': '注册失败'
            }
            print("管理员注册失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def hr_register(self, request, *args, **kwargs):
        print("用户请求了注册")
        data = request.data
        userId = data['userId']
        username = data['username']
        password = data['password']
        phone = data['phone']
        try:
            age = data['age']
        except Exception:
            age = 0

        try:
            gender = data['gender']
        except Exception:
            gender = '男'

        try:
            account = data['account']
        except Exception:
            account = ""

        try:
            bank = data['bank']
        except Exception:
            bank = ""

        try:
            bankCard = data['bankCard']
        except Exception:
            bankCard = ""

        try:
            accountHolderName = data['accountHolderName']
        except Exception:
            accountHolderName = ""

        try:
            idCard = data['idCard']
        except Exception:
            idCard = ""

        try:
            hr = EvaluationUser.objects.create_user(
                userId=userId,
                username=username,
                phone=phone,
                age=age,
                gender=gender,
                account=account,
                bank=bank,
                bankCard=bankCard,
                accountHolderName=accountHolderName,
                idCard=idCard,
                isAdmin=False
            )
            hr.set_password(password)
            hr.save()
            resp = {
                'status': True,
                'message': '注册成功'
            }
            print("用户注册成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '注册失败' + str(e)
            }
            print("用户注册失败" + str(e))
        return Response(resp)

    # 修改密码
    #################################################

    @action(detail=False, methods=['post'])
    def change_password(self, request, *args, **kwargs):
        print("用户请求了修改密码")
        data = request.data
        userId = data['userId']
        oldPassword = data['oldPassword']
        newPassword = data['newPassword']
        try:
            user = EvaluationUser.objects.get(userId=userId)
            if user.check_password(oldPassword):
                user.set_password(newPassword)
                user.save()
                resp = {
                    'status': True,
                    'message': '修改成功'
                }
                print("用户修改密码成功")
            else:
                resp = {
                    'status': False,
                    'message': '密码错误'
                }
                print("用户修改密码失败，密码错误")
        except:
            resp = {
                'status': False,
                'message': '用户不存在'
            }
            print("用户修改密码失败，用户不存在")
        return Response(resp)

    # 注销账号
    #################################################

    @action(detail=False, methods=['post'])
    def delete_student(self, request, *args, **kwargs):
        print("管理员请求了删除学生")
        data = request.data
        studentId = data['userId']
        try:
            student = EvaluationUser.objects.get(userId=studentId)
            userImages = UserImage.objects.filter(user=student)
            for userImage in userImages:
                userImage.image.delete()
                userImage.delete()  # 删除学生图片

            activities = Activity.objects.filter(student=student)
            for activity in activities:
                activityImages = ActivityImage.objects.filter(activity=activity)
                for activityImage in activityImages:
                    activityImage.image.delete()
                    activityImage.delete()  # 删除活动图片
                activity.delete()  # 删除活动
            student.delete()
            resp = {
                'status': True,
                'message': '删除成功'
            }
            print("管理员删除学生成功")
        except:
            resp = {
                'status': False,
                'message': '删除失败'
            }
            print("管理员删除学生失败")
        return Response(resp)

    @action(detail=False, methods=['get'])
    def get_salary_info(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'status': False,
                'message': '请先登录'
            })
        settled_count = request.user.getSettlementInterview().count()
        settlements = Settlement.objects.filter(user=request.user)
        total_received = sum(s.amount for s in settlements)
        
        # 新增：使用用户定义的发薪日变量，默认15
        pay_day = request.user.payDay.day if request.user.payDay else 15

        today = timezone.now()
        if today.day < pay_day:
            # 计算上个月从1日到pay_day的数据
            prev_month = today - relativedelta(months=1)
            period_start = prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = prev_month.replace(day=pay_day, hour=23, minute=59, second=59, microsecond=999999)
            count = Interview.objects.filter(
                user=request.user,
                settlement=False,
                isArrived=True,
                interviewTime__range=(period_start, period_end)
            ).count()
        else:
            # 当前月份：从1日到pay_day作为基础期
            current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            base_period_start = current_month
            base_period_end = today.replace(day=pay_day, hour=23, minute=59, second=59, microsecond=999999)
            base_count = Interview.objects.filter(
                user=request.user,
                settlement=False,
                isArrived=True,
                interviewTime__range=(base_period_start, base_period_end)
            ).count()
            if today.day > pay_day:
                extra_period_start = today.replace(day=pay_day+1, hour=0, minute=0, second=0, microsecond=0)
                extra_period_end = today  # up to current moment
                extra_count = Interview.objects.filter(
                    user=request.user,
                    settlement=False,
                    isArrived=True,
                    interviewTime__range=(extra_period_start, extra_period_end)
                ).count()
            else:
                extra_count = 0
            count = base_count + extra_count

        calculated_amount_due = count * salaryrate

        resp = {
            'status': True,
            'data': {
                'username': request.user.username,
                'unsettled_interviews': request.user.getUnSettlementInterview().count(),
                'settled_interviews': settled_count,
                'amount_due': calculated_amount_due,
                'amount_received': total_received,
                'salary_rate': salaryrate,
                'payDay': request.user.payDay,
            },
            'message': '获取报酬信息成功'
        }
        return Response(resp)

    # 在线HR相关接口
    #################################################

    @action(detail=False, methods=['get'])
    def get_hr_list(self, request, *args, **kwargs):
        print("用户请求了获取在线HR")
        try:
            users = EvaluationUser.objects.all()
            hr = users.filter(isAdmin=False)
            resp = {
                'status': True,
                'data': [_.to_dict() for _ in hr],
            }
            print("用户获取在线HR列表成功")
        except:
            resp = {
                'status': False,
                'data': '获取失败'
            }
            print("用户获取在线HR列表失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def hr_update(self, request, *args, **kwargs):
        print("用户请求了更新")
        data = request.data
        userId = data['userId']
        username = data['username']
        phone = data['phone']
        try:
            hr = EvaluationUser.objects.get(userId=userId)
            hr.username = username
            hr.phone = phone
            hr.age = data['age']
            hr.gender = data['gender']
            hr.bankCard = data['bankCard']
            hr.bank = data['bank']
            hr.accountHolderName = data['accountHolderName']
            hr.idCard = data['idCard']
            hr.account = data['account']
            hr.city = data['city']

            hr.save()
            resp = {
                'status': True,
                'message': '更新成功'
            }
            print("用户更新成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '更新失败' + str(e)
            }
            print("用户更新失败" + str(e))
        return Response(resp)

    # 用户信息
    @action(detail=False, methods=['get'])
    def user_info(self, request, *args, **kwargs):
        print("用户请求了个人信息")

        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return Response({"status": False, "message": "未登录"}, status=401)

        try:
            # 从数据库获取用户信息
            user = EvaluationUser.objects.get(userId=request.user.userId)

            # 组织返回数据
            resp = {
                "status": True,
                "data": {
                    "userId": user.userId,
                    "username": user.username,
                    "phone": user.phone,
                    "age": user.age,
                    "gender": user.gender,
                    "bankCard": user.bankCard,
                    "bank": user.bank,
                    "accountHolderName": user.accountHolderName,
                    "idCard": user.idCard,
                    "account": user.account,
                    "city": user.city,
                    "payDay": user.payDay,
                },

                "message": "用户信息获取成功"
            }
            print(resp)
            print("用户信息返回成功")

        except EvaluationUser.DoesNotExist:
            resp = {
                "status": False,
                "message": "用户信息不存在"
            }
            print("用户信息获取失败")
        return Response(resp)

    # 题库相关接口
    #################################################

    @action(detail=False, methods=['post'])
    def create_question(self, request, *args, **kwargs):
        print("用户请求了新建题目")

        # 读取并解析上传的 JSON 文件
        json_file = request.FILES.get("json")
        if (json_file):
            data = json.loads(json_file.read().decode('utf-8'))
        else:
            return Response({"status": False, "message": "没有上传JSON文件"})

        # 获取上传的文件
        file = request.FILES.get("file")
        if not file:
            return Response({"status": False, "message": "没有上传文件"})

        # post = data.get('post')
        answer = data.get('answer')
        mainProblem = data.get('mainProblem')
        problemDescription = data.get('problemDescription')

        try:
            # 创建题目对象
            question = CurriculumVitae.objects.create(
                # post=post,
                qualified=answer,
                mainProblem=mainProblem,
                problemDescription=problemDescription,
                file=file  # 文件会自动保存到 MEDIA_ROOT 目录
            )
            question.save()

            resp = {
                'status': True,
                'message': '新建题目成功',
                'data': {
                    'questionId': question.id
                }
            }
            print("用户新建题目成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '新建题目失败',
                'error': str(e)  # 将错误信息返回，方便调试
            }
            print("用户新建题目失败:", e)

        return Response(resp)

    @action(detail=False, methods=['post'])
    def question_update(self, request, *args, **kwargs):
        print("用户请求了题目更新")
        data = request.data
        questionId = data['id']
        # questionPost = data['post']
        questionAnswer = data['qualified']
        questionMainProblem = data['mainProblem']
        questionProblemDescription = data['problemDescription']
        try:
            question = CurriculumVitae.objects.get(id=questionId)
            # question.post = questionPost
            question.qualified = questionAnswer
            question.mainProblem = questionMainProblem
            question.problemDescription = questionProblemDescription
            question.save()
            resp = {
                'status': True,
                'message': '更新成功'
            }
            print("用户更新成功")
        except:
            resp = {
                'status': False,
                'message': '更新失败'
            }
            print("用户更新失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def delete_question(self, request, *args, **kwargs):
        print("管理员请求了删除学生")
        data = request.data
        questionId = data['questionId']
        try:
            question = CurriculumVitae.objects.get(id=questionId)
            question.delete()
            resp = {
                'status': True,
                'message': '删除成功'
            }
            print("管理员删除学生成功")
        except:
            resp = {
                'status': False,
                'message': '删除失败'
            }
            print("管理员删除学生失败")
        return Response(resp)

    @action(detail=False, methods=['get'])
    def get_question_list(self, request, *args, **kwargs):
        print("用户请求了获取题目列表")
        try:
            question_list = CurriculumVitae.objects.all()
            questionList = []
            for index, item in enumerate(question_list):
                post = item.post
                qualified = item.qualified
                file_url = item.file.url
                questionList.append({
                    'id': item.id,
                    'post': post,
                    'qualified': qualified,
                    'file_url': file_url,
                    'create_time': item.createTime,
                    'num_test': item.numTest,
                    'pass_time': item.passTime,
                    'pass_rate': item.getPassRate(),
                    'main_problem': item.mainProblem,
                    'problem_description': item.problemDescription
                })

            resp = {
                'status': True,
                'data': questionList,
            }
            print("用户获取题目列表成功")
        except Exception as e:
            resp = {
                'status': False,
                'data': '获取失败' + str(e)
            }
            print("用户获取题目列表失败" + str(e))
        return Response(resp)

    @action(detail=False, methods=['get'])
    def get_exam_question_list(self, request, *args, **kwargs):
        print("用户请求了获取测试题目列表")
        data = request.data
        try:
            question_list = CurriculumVitae.objects.filter()
            # 随机获取10道题
            test_question_list = question_list.order_by('?')[:10]
            testQuestionList = []
            for index, item in enumerate(test_question_list):
                file_url = item.file.url
                testQuestionList.append({
                    'id': item.id,
                    'post': item.post,
                    'qualified': item.qualified,
                    'file_url': file_url,
                    'create_time': item.createTime,
                    'num_test': item.numTest,
                    'pass_time': item.passTime,
                    'pass_rate': item.getPassRate(),
                    'main_problem': item.mainProblem,
                    'problem_description': item.problemDescription
                })

            resp = {
                'status': True,
                'data': testQuestionList,
            }
            print("用户获取测试题目列表成功")
        except Exception as e:
            resp = {
                'status': False,
                'data': '获取失败' + str(e)
            }
            print("用户获取测试题目列表失败" + str(e))
        return Response(resp)

    @action(detail=False, methods=['post'])
    def post_question_image(self, request, *args, **kwargs):
        print("用户请求了提交简历")
        data = request.data
        questionId = data['questionId']
        image = request.FILES['image']
        try:
            question = CurriculumVitae.objects.get(id=questionId)
            if question.file:
                if os.path.isfile(question.file.path):
                    os.remove(question.file.path)
            question.file = image
            question.save()
            resp = {
                'status': True,
                'message': '提交成功'
            }
            print("用户提交简历成果")
        except Exception as e:
            resp = {
                'status': False,
                'message': '提交失败' + str(e)
            }
            print("用户提交简历失败" + str(e))
        return Response(resp)

    @action(detail=False, methods=['post'])
    def post_exam_result(self, request, *args, **kwargs):
        print("用户请求了提交测试结果")
        data = request.data
        good_answer = 0
        try:
            for _ in data:
                question = CurriculumVitae.objects.get(id=_['questionId'])
                question.numTest += 1
                if question.qualified == _['answer']:
                    question.passTime += 1
                    good_answer += 1
                question.save()
            resp = {
                'status': True,
                'data': good_answer,
                'message': '提交答案成功'
            }
            print("用户提交提交答案成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '提交答案失败' + str(e)
            }
            print("用户提交答案失败" + str(e))
        return Response(resp)

    # 约面管理相关接口
    #################################################

    @action(detail=False, methods=['post'])
    def create_interview(self, request, *args, **kwargs):
        print("用户请求了新建面试")

        # 读取并解析上传的 JSON 文件
        json_file = request.FILES.get("json")
        if (json_file):
            data = json.loads(json_file.read().decode('utf-8'))
        else:
            return Response({"status": False, "message": "没有上传JSON文件"})

        # 获取上传的文件
        file = request.FILES.get("file")
        if not file:
            return Response({"status": False, "message": "没有上传文件"})
        #         'name'       : interview_name.value,
        #         'post'       : interview_post.value,
        #         'commuteTime': inetrvew_commute_time.value,
        #         'time'       : interview_time.value,
        #         'hr'         : hr_username.value,
        name = data.get('name')
        post = data.get('post')
        commuteTime = data.get('commuteTime')
        time = data.get('time')
        hr = EvaluationUser.objects.get(username=data.get('hr'))

        try:
            # 创建题目对象
            interview = Interview.objects.create(
                interviewee=name,
                interviewTime=time,
                post=post,
                user=hr,
                commuteTime=commuteTime
            )
            interview.save()

            curriculumVitae = CurriculumVitae.objects.create(
                interview=interview,
                post=post,
                file=file,
                qualified=True
            )
            curriculumVitae.save()
            resp = {
                'status': True,
                'message': '新建约面成功',
                'data': {
                    'questionId': interview.id
                }
            }
            print("用户新建约面成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '新建约面失败',
                'error': str(e)  # 将错误信息返回，方便调试
            }
            print("用户新建约面失败:", e)

        return Response(resp)

    @action(detail=False, methods=['get'])
    def get_interview_list(self, request, *args, **kwargs):
        print("用户请求了获取约面列表")
        try:
            interview_list = Interview.objects.all().order_by('-createTime')
            interviewList = []
            for index, item in enumerate(interview_list):
                interviewList.append(item.to_dict())
                # file = CurriculumVitae.objects.get(interview=item)
                # file_url = file.file.url
                # interviewList.append({
                #     'id': item.id,
                #     'post': item.post,
                #     'name': item.interviewee,
                #     'hr': item.user.username,
                #     'interview_time': item.interviewTime,
                #     'file_url': file_url,
                #     'create_time': item.createTime,
                #     'commuteTime': item.commuteTime,
                #     'isAgreed': item.isAgreed,
                #     'isArrived': item.isArrived,
                #     'settlement': item.settlement
                # })
            resp = {
                'status': True,
                'data': interviewList,
            }
            print("用户获取约面列表成功")
        except Exception as e:
            resp = {
                'status': False,
                'data': '获取失败' + str(e)
            }
            print("用户获取约面列表失败" + str(e))
        return Response(resp)

    # 获取当前用户创建的所有面试信息
    @action(detail=False, methods=['post'])
    def get_user_interview_list(self, request, *args, **kwargs):
        print("用户请求了获取个人约面列表")
        data = request.data
        try:
            # 获取当前登录用户
            userId = data['userId']
            current_user = EvaluationUser.objects.get(userId=userId)
            # 只获取当前用户创建的面试信息
            interview_list = Interview.objects.filter(user=current_user)

            interviewList = []
            for index, item in enumerate(interview_list):
                interviewList.append(item.to_dict())

            resp = {
                'status': True,
                'data': interviewList,
            }
            print(f"用户'{current_user.username}'获取个人约面列表成功，共{len(interviewList)}条记录")
        except Exception as e:
            resp = {
                'status': False,
                'data': '获取失败：' + str(e)
            }
            print("用户获取个人约面列表失败：" + str(e))

        return Response(resp)

    @action(detail=False, methods=['post'])
    def post_curriculumVitae_image(self, request, *args, **kwargs):
        print("用户请求了提交约面者简历")
        data = request.data
        interviewId = data['interviewId']
        file = request.FILES['file']
        try:
            interview = Interview.objects.get(id=interviewId)
            if CurriculumVitae.objects.filter(interview=interview).count() > 0:
                curriculumVitae = CurriculumVitae.objects.get(interview=interview)
                curriculumVitae.file.delete()
                curriculumVitae.delete()
            curriculumVitae = CurriculumVitae.objects.create(
                interview=interview,
                post=interview.post,
                file=file
            )
            curriculumVitae.save()
            resp = {
                'status': True,
                'message': '提交成功'
            }
            print("用户提交面试者简历成功")
        except:
            resp = {
                'status': False,
                'message': '提交失败'
            }
            print("用户提交面试者简历成功失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def interview_update(self, request, *args, **kwargs):
        print("用户请求了更新")
        data = request.data
        interviewId = data['id']
        interviewee = data['name']
        hr = EvaluationUser.objects.get(username=data['hr'])
        interviewTime = data['interview_time']
        commuteTime = data['commuteTime']
        post = data['post']
        isAgreed = data['isAgreed']
        isArrived = data['isArrived']
        try:
            interview = Interview.objects.get(id=interviewId)
            interview.user = hr
            interview.interviewee = interviewee
            interview.interviewTime = interviewTime
            interview.commuteTime = commuteTime
            interview.post = post
            interview.isAgreed = isAgreed
            interview.isArrived = isArrived
            interview.save()
            resp = {
                'status': True,
                'message': '更新成功'
            }
            print("用户更新成功")
        except:
            resp = {
                'status': False,
                'message': '更新失败'
            }
            print("用户更新失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def delete_interview(self, request, *args, **kwargs):
        print("管理员请求了删除面试")
        data = request.data
        interviewId = data['interviewId']
        try:
            interview = Interview.objects.get(id=interviewId)
            curriculumVitae = CurriculumVitae.objects.get(interview=interview)

            curriculumVitae.delete()
            interview.delete()

            resp = {
                'status': True,
                'message': '删除成功'
            }
            print("管理员删除面试成功")
        except:
            resp = {
                'status': False,
                'message': '删除失败'
            }
            print("管理员删除面试失败")
        return Response(resp)


    # 报酬管理接口
    #################################################

    @action(detail=False, methods=['get'])
    def get_salary_list(self, request, *args, **kwargs):
        print("用户请求了获取未结算列表")
        try:
            interview_list = Interview.objects.filter(settlement=False, isArrived=True)
            salaryList = []
            hrList = []
            for index, item in enumerate(interview_list):
                hr = item.user
                if hr not in hrList:
                    hrList.append(hr)

            for index, item in enumerate(hrList):

                userInterviewList = item.getUnSettlementInterview()
                userInterviewListJson = []
                salaryInformation = {
                    'num': 0,
                    'price': 0,
                }
                for userInterview in userInterviewList:
                    userInterviewListJson.append(userInterview.to_dict())
                    salaryInformation['num'] += 1
                    salaryInformation['price'] += 100

                salaryList.append({
                    'hr': item.to_dict(),
                    'interviewList': userInterviewListJson,
                    'salaryInformation': salaryInformation,
                })

            resp = {
                'status': True,
                'data': salaryList,
            }
            print("用户获取未结算列表成功")
        except Exception as e:
            resp = {
                'status': False,
                'data': '获取失败' + str(e)
            }
            print("用户获取未结算列表失败" + str(e))
        return Response(resp)

    @action(detail=False, methods=['post'])
    def post_settlement(self, request, *args, **kwargs):
        print("用户请求了结算")
        data = request.data
        interviewIdList = data['interviewIdList']
        hr = EvaluationUser.objects.get(userId=data['hrId'])
        num = int(data['num'])
        try:
            for interviewId in interviewIdList:
                interview = Interview.objects.get(id=interviewId)
                interview.settlement = True
                interview.save()
            settlement = Settlement.objects.create(
                user=hr,
                amount=num * 100,
                bankCard=hr.bankCard,
                bank=hr.bank,
                accountHolderName=hr.accountHolderName,
                idCard=hr.idCard,
            )
            settlement.save()
            hr.payDay = hr.payDay = (datetime.now() + relativedelta(months=1)).date()
            #hr.payDay = datetime.now()
            hr.save()
            resp = {
                'status': True,
                'message': '结算成功'
            }
            print("用户结算成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '结算失败' + str(e)
            }
            print("用户结算失败" + str(e))
        return Response(resp)

    @action(detail=False, methods=['post'])
    def post_settle_all(self, request, *args, **kwargs):
        print("用户请求了全部结算")
        try:

            hrList = EvaluationUser.objects.all()
            for hr in hrList:
                num = hr.getUnSettlementInterview().count()
                if num > 0:
                    settlement = Settlement.objects.create(
                        user=hr,
                        amount=num * 100,
                        bankCard=hr.bankCard,
                        bank=hr.bank,
                        accountHolderName=hr.accountHolderName,
                        idCard=hr.idCard,
                    )
                    settlement.save()
                    interview_list = Interview.objects.filter(user=hr, settlement=False)
                    for interview in interview_list:
                        interview.settlement = True
                        interview.save()
                    hr.payDay = datetime.now()

            resp = {
                'status': True,
                'message': '全部结算成功'
            }
            print("用户全部结算成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '全部结算失败' + str(e)
            }
            print("用户全部结算失败" + str(e))
        return Response(resp)

    # 流水管理接口
    #################################################

    @action(detail=False, methods=['get'])
    def get_settlement_list(self, request, *args, **kwargs):
        print("用户请求了获取流水列表")
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return Response({'status': False, 'message': '请先登录'})
        try:
            # 仅获取当前用户的结算记录
            settlement_list = Settlement.objects.filter(user=request.user).order_by("-settlementTime")
            settlementList = []
            for item in settlement_list:
                settlementList.append(item.to_dict())
            resp = {
                'status': True,
                'data': settlementList,
            }
            print("用户获取流水列表成功")
        except Exception as e:
            resp = {
                'status': False,
                'data': '获取失败' + str(e)
            }
            print("用户获取流水列表失败" + str(e))
        return Response(resp)

    # 活动相关接口（已废弃）
    #################################################

    @action(detail=False, methods=['post'])
    def create_activity(self, request, *args, **kwargs):
        print("用户请求了提交活动")
        # data = json.loads(request.body)
        data = request.data
        name = data['name']
        description = data['description']
        startTime = data['startTime']
        endTime = data['endTime']
        location = data['location']
        studentId = data['studentId']
        activityType = data['type']
        try:
            student = EvaluationUser.objects.get(userId=studentId)
            activity = Activity.objects.create(name=name, description=description, startTime=startTime, endTime=endTime,
                                               location=location, student=student, type=activityType)
            activity.save()
            student.save()
            resp = {
                'status': True,
                'message': '提交成功',
                'data': {
                    'activityId': activity.id
                }
            }
            print("用户提交活动成功")
        except:
            resp = {
                'status': False,
                'message': '提交失败'
            }
            print("用户提交活动失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def get_activities_list(self, request, *args, **kwargs):
        print("用户请求了获取活动")
        data = request.data
        # data = json.loads(request.data)
        studentId = data['studentId']
        startTime = data['startTime']
        endTime = data['endTime']
        certified = data['certified']
        passed = data['passed']
        adminId = data['adminId']
        try:
            activities = Activity.objects.all()
            if studentId != '*' and studentId != '':
                student = EvaluationUser.objects.get(userId=studentId)
                activities = activities.filter(student=student)
            if (startTime != '*' and endTime != '*') and (startTime != '' and endTime != ''):
                activities = activities.filter(startTime__gte=startTime, endTime__lte=endTime)
            if certified != '*' and certified != '':
                activities = activities.filter(certified=certified)
            if passed != '*' and passed != '':
                activities = activities.filter(passed=passed)
            if adminId != '*' and adminId != '':
                admin = EvaluationUser.objects.get(userId=adminId)
                activities = activities.filter(admin=admin)
            resp = {
                'status': True,
                'data': json.loads(serialize('json', activities)),
                'message': '获取活动列表成功'
            }
            print("用户获取活动成功")
        except:
            resp = {
                'status': False,
                'message': '获取活动列表失败'
            }
            print("用户获取活动失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def get_activity_images(self, request, *args, **kwargs):
        print("用户请求了获取活动图片")
        data = request.data
        activityId = data['activityId']
        try:
            activity = Activity.objects.get(id=activityId)
            images = ActivityImage.objects.filter(activity=activity)
            resp = {
                'status': True,
                'data': json.loads(serialize('json', images)),
                'message': '获取成功'
            }
            print("用户获取活动图片成功")
        except:
            resp = {
                'status': False,
                'message': '获取失败'
            }
            print("用户获取活动图片失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def post_activity_image(self, request, *args, **kwargs):
        print("用户请求了提交活动图片")
        data = request.data
        activityId = data['activityId']
        image = request.FILES['image']
        try:
            activity = Activity.objects.get(id=activityId)
            activityImage = ActivityImage.objects.create(activity=activity, image=image)
            activityImage.save()
            resp = {
                'status': True,
                'message': '提交成功'
            }
            print("用户提交活动图片成功")
        except:
            resp = {
                'status': False,
                'message': '提交失败'
            }
            print("用户提交活动图片失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def delete_activity(self, request, *args, **kwargs):
        print("用户请求了删除活动")
        data = request.data
        activityId = data['activityId']
        try:
            activity = Activity.objects.get(id=activityId)
            student = activity.student
            activityImages = ActivityImage.objects.filter(activity=activity)
            for activityImage in activityImages:
                activityImage.image.delete()
                activityImage.delete()  # 删除活动图片
            activity.delete()
            student.score_test1 -= 1
            student.save()
            resp = {
                'status': True,
                'message': '删除成功'
            }
            print("用户删除活动成功")
        except:
            resp = {
                'status': False,
                'message': '删除失败'
            }
            print("用户删除活动失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def check_activity(self, request, *args, **kwargs):
        print("用户请求了查看活动")
        data = request.data
        adminId = data['adminId']
        activityId = data['activityId']
        passed = data['passed']
        if passed == 'true':
            passed = True
        else:
            passed = False
        try:
            admin = EvaluationUser.objects.get(userId=adminId)
            activity = Activity.objects.get(pk=activityId)
            if activity.passed:
                resp = {
                    'status': False,
                    'message': '已经审核过了'
                }
                print("用户查看活动失败，已审核")
                return Response(resp)
            activity.passed = passed
            activity.certified = True
            activity.admin = admin
            activity.save()
            resp = {
                'status': True,
                'data': json.loads(serialize('json', [activity])),
                'message': '审核成功'
            }
            print("用户查看活动成功")
        except:
            resp = {
                'status': False,
                'message': '审核失败'
            }
            print("用户查看活动失败")
        return Response(resp)

    # 工具接口
    #################################################

    @action(detail=False, methods=['post'])
    def post_user_image(self, request, *args, **kwargs):
        print("用户请求了提交用户图片")
        data = request.data
        userId = data['userId']
        image = request.FILES['image']
        try:
            user = EvaluationUser.objects.get(userId=userId)
            if UserImage.objects.filter(user=user).count() > 0:
                userImage = UserImage.objects.get(user=user)
                userImage.image.delete()
                userImage.delete()
            userImage = UserImage.objects.create(user=user, image=image)
            userImage.save()
            resp = {
                'status': True,
                'message': '提交成功'
            }
            print("用户提交用户图片成功")
        except Exception as e:
            resp = {
                'status': False,
                'message': '提交失败' + str(e)
            }
            print("用户提交用户图片失败" + str(e))
        return Response(resp)

    @action(detail=False, methods=['post'])
    def get_user_image(self, request, *args, **kwargs):
        print("用户请求了获取活动图片")
        data = request.data
        userId = data['userId']
        try:
            user = EvaluationUser.objects.get(userId=userId)
            images = UserImage.objects.filter(user=user)
            resp = {
                'status': True,
                'data': json.loads(serialize('json', images)),
                'message': '获取成功'
            }
            print("用户获取用户图片成功")
        except:
            resp = {
                'status': False,
                'message': '获取失败'
            }
            print("用户获取用户图片失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def get_curriculumVitae_image(self, request, *args, **kwargs):
        print("用户请求了获取简历图片")
        data = request.data
        userId = data['userId']
        try:
            user = EvaluationUser.objects.get(userId=userId)
            images = CurriculumVitae.objects.filter(user=user)
            resp = {
                'status': True,
                'data': json.loads(serialize('json', images)),
                'message': '获取成功'
            }
            print("用户获取用户图片成功")
        except:
            resp = {
                'status': False,
                'message': '获取失败'
            }
            print("用户获取用户图片失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def export_excel(self, request, *args, **kwargs):
        print("用户请求了导出excel")
        data = request.data
        studentId = data['studentId']
        try:
            if studentId == '*':
                activities = Activity.objects.all()
            else:
                student = EvaluationUser.objects.get(userId=studentId)
                activities = Activity.objects.filter(student=student)

            return generate_excel(activities)
            # resp = {
            #     'status': True,
            #     'data': generate_excel(activities),
            #     'message': '导出成功'
            # }
            # print("用户导出excel成功")
        except:
            resp = {
                'status': False,
                'message': '导出失败'
            }
            print("用户导出excel失败")
        return Response(resp)

    @action(detail=False, methods=['post'])
    def reset(self, request, *args, **kwargs):
        print("用户请求了重置")
        data = request.data
        superPassword = data['superPassword']
        if superPassword == '22201076':
            resp = {
                'status': False,
                'message': '你想干啥'
            }
            return Response(resp)
        resetType = data['resetType']

        if resetType == 'settlement':
            settlementList = Settlement.objects.all()
            for settlement in settlementList:
                settlement.delete()