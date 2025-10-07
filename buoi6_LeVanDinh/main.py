import mysql.connector
from lxml import etree
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
 database="mydatabase"
)

mydinh = mydb.cursor()
mydinh.execute("""
    Create table if not exists Categories(
    id Varchar(10) Primary Key,
    name Varchar(255) Not Null
    )
""")
mydinh.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    stock INT NOT NULL,
    categoryRef VARCHAR(10),
    FOREIGN KEY (categoryRef) REFERENCES Categories(id)
)
""")

def validate_xml(xml_file, xsd_file):
    """Validate XML với XSD schema"""
    try:
        # Tạo XMLSchema object từ XSD
        with open(xsd_file, 'rb') as f:
            xsd_doc = etree.parse(f)
            xsd = etree.XMLSchema(xsd_doc)
        
        # Parse file XML
        with open(xml_file, 'rb') as f:
            xml_doc = etree.parse(f)
        
        # Validate XML với XSD
        if xsd.validate(xml_doc):
            print("✅ XML hợp lệ!")
            return xml_doc  # ← QUAN TRỌNG: trả về xml_doc, không phải True
        else:
            print("❌ XML không hợp lệ! Lỗi cụ thể:")
            for error in xsd.error_log:
                print(f"  - Dòng {error.line}: {error.message}")
            return None
            
    except Exception as e:
        print(f"❌ Lỗi validate XML: {e}")
        return None
def process_categories_and_products(xml_doc):
    """Dùng XPath để lấy dữ liệu và insert vào MySQL"""
    
    # === XỬ LÝ CATEGORIES ===
    categories = xml_doc.xpath('//categories/category')
    print(f"Tìm thấy {len(categories)} categories")
    
    for category in categories:
        category_id = category.get('id')
        category_name = category.text
        
        # Insert vào bảng Categories (nếu id đã có thì cập nhật)
        sql = """
        INSERT INTO Categories (id, name) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
        """
        mydinh.execute(sql, (category_id, category_name))
        print(f"✅ Đã xử lý category: {category_id} - {category_name}")
    
    # === XỬ LÝ PRODUCTS ===
    products = xml_doc.xpath('//products/product')
    print(f"Tìm thấy {len(products)} products")
    
    for product in products:
        product_id = product.get('id')
        category_ref = product.get('categoryRef')
        
        # Dùng XPath để lấy thông tin sản phẩm
        name = product.xpath('name/text()')[0]
        price = product.xpath('price/text()')[0]
        currency = product.xpath('price/@currency')[0]
        stock = product.xpath('stock/text()')[0]
        
        # Insert vào bảng Products (nếu id đã có thì cập nhật)
        sql = """
        INSERT INTO Products (id, name, price, currency, stock, categoryRef) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            name = VALUES(name),
            price = VALUES(price),
            currency = VALUES(currency),
            stock = VALUES(stock),
            categoryRef = VALUES(categoryRef)
        """
        mydinh.execute(sql, (product_id, name, price, currency, stock, category_ref))
        print(f"✅ Đã xử lý product: {product_id} - {name}")
    
    # Commit transaction
    mydb.commit()
    print(f"🎉 Đã xử lý thành công {len(categories)} categories và {len(products)} products!")
    
def display_results():
    """Hiển thị kết quả sau khi xử lý"""
    print("\n📊 KẾT QUẢ:")
    
    # Hiển thị Categories
    mydinh.execute("SELECT * FROM Categories")
    categories = mydinh.fetchall()
    print("\n📁 CATEGORIES:")
    for cat in categories:
        print(f"  {cat[0]}: {cat[1]}")
    
    # Hiển thị Products
    mydinh.execute("SELECT * FROM Products")
    products = mydinh.fetchall()
    print("\n📦 PRODUCTS:")
    for prod in products:
        print(f"  {prod[0]}: {prod[1]} - ${prod[2]} {prod[3]} - Stock: {prod[4]} - Category: {prod[5]}")    
if __name__ == "__main__":
    # Validate XML với XSD
    xml_doc = validate_xml("./buoi6_LeVanDinh/catalog.xml", "./buoi6_LeVanDinh/schema.xsd")
    
    # Nếu hợp lệ thì xử lý dữ liệu
    if xml_doc:
        process_categories_and_products(xml_doc)
        display_results()
    
    # Đóng kết nối
    mydinh.close()
    mydb.close()
    print("\n🔚 Đã đóng kết nối database.")    