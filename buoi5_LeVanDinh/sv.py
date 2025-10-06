import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from lxml import etree
tree = etree.parse('./buoi5_LeVanDinh/sv.xml')
# 1. In ra tất cả sinh viên
print("1. TẤT CẢ SINH VIÊN:")
students = tree.xpath("//student")
for student in students:
    id = student.xpath("id/text()")[0]
    name = student.xpath("name/text()")[0]
    date = student.xpath("date/text()")[0]
    print(f"   - {id}: {name} | {date}")
#2 Tên tất cả sinh viên
print("\n2. TÊN TẤT CẢ SINH VIÊN:")
names = tree.xpath("//student/name/text()")
for name in names:
    print(f"    - {name}")
#3 Lấy tất cả id của sinh viên    
print("\n3. ID TẤT CẢ SINH VIÊN:")
ids = tree.xpath("//student/id/text()")
for id in ids:
    print(f"    - {id}")
#4 Lấy ngày sinh của sinh viên có id = "SV01"
date_sv01  = tree.xpath("//student[id='SV01']/date/text()")    
print("\n4. NGÀY SINH CỦA SINH VIÊN CÓ ID = 'SV01':")
print(f"    - {date_sv01[0]}")
#5 Lấy các khóa học
print("\n5. KHÓA HỌC CỦA TẤT CẢ SINH VIÊN:")
courses = tree.xpath("//enrollment/course/text()")
for course in courses:
    print(f"    - {course}")
#6 Lấy toàn bộ thông tin của sinh viên đầu tiên
first_student = tree.xpath("//student[1]")[0]
student_id = first_student.xpath("id/text()")[0]

id = first_student.xpath("id/text()")[0]
name = first_student.xpath("name/text()")[0]
date = first_student.xpath("date/text()")[0]
courses = tree.xpath(f"//enrollment[studentRef='{student_id}']/course/text()")
print("\n6. THÔNG TIN CỦA SINH VIÊN ĐẦU TIÊN:")
print(f"    - ID: {id}")
print(f"    - Name: {name}")
print(f"    - Date: {date}")
print(f"   Môn học đã đăng ký: {', '.join(courses) if courses else 'Chưa đăng ký'}")
#7 Lấy mã sinh viên đăng ký khóa học "Vatly203"
students_vatly203 = tree.xpath("//enrollment[course='Vatly203']/studentRef/text()")
print("\n7. MÃ SINH VIÊN ĐĂNG KÝ KHÓA HỌC 'Vatly203':")
for student_id in students_vatly203:
    print(f"    - {student_id}")
# 8 Lấy tên sinh viên học môn "Toan101"
students_toan101 = tree.xpath("//enrollment[course='Toan101']/studentRef/text()")
print("\n8. TÊN SINH VIÊN HỌC MÔN 'Toan101':")
for student_id in students_toan101:
    name = tree.xpath(f"//student[id='{student_id}']/name/text()")[0]
    print(f"    - {name}")
#9 Lấy tên sinh viên học môn "Vatly203"
print("\n9. TÊN SINH VIÊN HỌC MÔN 'Vatly203':")
students_vatly203 =tree.xpath("//enrollment[course='Vatly203']/studentRef/text()")
for student_id in students_vatly203:
    name = tree.xpath(f"//student[id =  '{student_id}']/name/text()")[0] 
    print(f"    - {name}")   
#10 Lấy ngày sinh của sinh viên có id="SV01"
date_sv01 = tree.xpath("//student[id='SV01']/date/text()")
print("\n10. NGÀY SINH CỦA SINH VIÊN CÓ ID = 'SV01':")
print(f"    - {date_sv01[0]}")
#11  Lấy tên và ngày sinh của mọi sinh viên sinh năm 1997
students_1997 = tree.xpath("//student[contains(date, '1997')]")
print("\n11. TÊN VÀ NGÀY SINH CỦA MỌI SINH VIÊN SINH NĂM 1997:")
for student in students_1997:
    name = student.xpath("name/text()")[0]
    date = student.xpath("date/text()")[0]
    print(f"    - {name} | {date}")
#12 Lấy tên của các sinh viên có ngày sinh trước năm 1998
students_before_1998 = tree.xpath("//student[substring(date, 1, 4) < '1998']")
print("\n12. TÊN CỦA CÁC SINH VIÊN CÓ NGÀY SINH TRƯỚC NĂM 1998:")
for student in students_before_1998:
    name = student.xpath("name/text()")[0]
    print(f"    - {name}")
#13 Đếm tổng số sinh viên
total_students = len(tree.xpath("//student"))
print(f"\n13. TỔNG SỐ SINH VIÊN: {total_students}")
#14 Lấy tất cả sinh viên chưa đăng ký môn nào
all_student_ids = set(tree.xpath("//student/id/text()"))
enrolled_student_ids = set(tree.xpath("//enrollment/studentRef/text()"))
unenrolled_student_ids = all_student_ids - enrolled_student_ids
print("\n14. TẤT CẢ SINH VIÊN CHƯA ĐĂNG KÝ MÔN NÀO:")
for student_id in unenrolled_student_ids:
    name = tree.xpath(f"//student[id='{student_id}']/name/text()")[0]
    print(f"    - {name} (ID: {student_id})")
#15 Lấy phần tử <date> anh em ngay sau <name> của SV01
date_after_name_sv01 = tree.xpath("//student[id='SV01']/name/following-sibling::date[1]/text()")
print("\n15. PHẦN TỬ <date> ANH EM NGAY SAU <name> CỦA SV01:")
print(f"    - {date_after_name_sv01[0] if date_after_name_sv01 else 'Không tìm thấy'}")
#16 Lấy phần tử <id> anh em ngay trước <name> của SV02
id_before_name_sv02 = tree.xpath("//student[id='SV02']/name/preceding-sibling::id[1]/text()")
print("\n16. PHẦN TỬ <id> ANH EM NGAY TRƯỚC <name> CỦA SV02:")
print(f"    - {id_before_name_sv02[0] if id_before_name_sv02 else 'Không tìm thấy'}")
#17Lấy toàn bộ node <course> trong cùng một <enrollment> với studentRef='SV03' 
courses_sv03 = tree.xpath("//enrollment[studentRef='SV03']/course/text()")
print("\n17. TOÀN BỘ NODE <course> TRONG CÙNG MỘT <enrollment> VỚI studentRef='SV03':") 
for course in courses_sv03:
    print(f"    - {course}")
#18 Lấy sinh viên có họ là “Trần”
students_tran = tree.xpath("//student[starts-with(name, 'Trần')]")
print("\n18. SINH VIÊN CÓ HỌ LÀ 'Trần':")
for student in students_tran:
    id = student.xpath("id/text()")[0]
    name = student.xpath("name/text()")[0]
    date = student.xpath("date/text()")[0]
    print(f"    - {id}: {name} | {date}")
#19 Lấy năm sinh của sinh viên SV01
year_sv01 = tree.xpath("substring(//student[id='SV01']/date/text(), 1, 4)")
print("\n19. NĂM SINH CỦA SINH VIÊN SV01:")
print(f"    - {year_sv01}")
          

    