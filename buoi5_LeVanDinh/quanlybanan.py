from lxml import etree
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# Đọc file XML
file_path = "./buoi5_LeVanDinh/quanlybanan.xml"
tree = etree.parse(file_path)

print("🎯 KẾT QUẢ XPATH - QUẢN LÝ BÀN ĂN")
print("=" * 50)

def test_xpath(expression, description):
    print(f"\n🔍 {description}")
    try:
        results = tree.xpath(expression)
        if results:
            for i, result in enumerate(results, 1):
                if hasattr(result, 'text') and result.text:
                    print(f"  {i}. {result.text.strip()}")
                elif hasattr(result, 'tag'):
                    # Hiển thị thông tin element
                    content = etree.tostring(result, encoding='unicode', method='text').strip()
                    if content:
                        print(f"  {i}. <{result.tag}>: {content}")
                    else:
                        print(f"  {i}. <{result.tag}>")
                else:
                    print(f"  {i}. {result}")
        else:
            print("  Không có kết quả")
    except Exception as e:
        print(f"  Lỗi: {e}")

# Test các XPath
test_cases = [
    ("//BAN", "1. Tất cả bàn"),
    ("//NHANVIEN", "2. Tất cả nhân viên"),
    ("//TENMON/text()", "3. Tất cả tên món"),
    ("//NHANVIEN[MANV='NV02']/TENV/text()", "4. Tên nhân viên NV02"),
    ("//NHANVIEN[MANV='NV03']/*[self::TENV or self::SDT]", "5. Tên và SDT NV03"),
    ("//MON[GIA > 50000]/TENMON/text()", "6. Món có giá > 50,000"),
    ("//HOADON[SOHD='HD03']/SOBAN/text()", "7. Số bàn của HD03"),
    ("//MON[MAMON='M02']/TENMON/text()", "8. Tên món M02"),
    ("//HOADON[SOHD='HD03']/NGAYLAP/text()", "9. Ngày lập HD03"),
    ("//HOADON[SOHD='HD01']//CTHD/MAMON/text()", "10. Mã món trong HD01"),
    ("//MON[MAMON=//HOADON[SOHD='HD01']//CTHD/MAMON]/TENMON/text()", "11. Tên món trong HD01"),
    ("//NHANVIEN[MANV=//HOADON[SOHD='HD02']/MANV]/TENV/text()", "12. Tên NV lập HD02"),
    ("count(//BAN)", "13. Đếm số bàn"),
    ("count(//HOADON[MANV='NV01'])", "14. Số hóa đơn NV01 lập"),
    ("//MON[MAMON=//HOADON[SOBAN='2']//CTHD/MAMON]/TENMON/text()", "15. Món trong HD bàn 2"),
    ("//NHANVIEN[MANV=//HOADON[SOBAN='3']/MANV]", "16. NV lập HD bàn 3"),
    ("//HOADON[MANV=//NHANVIEN[GIOITINH='Nữ']/MANV]", "17. HD NV nữ lập"),
    ("//NHANVIEN[MANV=//HOADON[SOBAN='1']/MANV]", "18. NV phục vụ bàn 1"),
    ("//CTHD[SOLUONG > 1]/../../..//MAMON/text()", "19. Món được gọi > 1 lần"),
]

for xpath, description in test_cases:
    test_xpath(xpath, description)