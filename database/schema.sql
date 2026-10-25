-- SQL Server production schema. The app's local SQLite database mirrors these entities for easy development.
CREATE TABLE Categories (CategoryID INT PRIMARY KEY, CategoryName NVARCHAR(80) NOT NULL UNIQUE);
CREATE TABLE Customers (CustomerID INT PRIMARY KEY, CustomerName NVARCHAR(120) NOT NULL UNIQUE, Region NVARCHAR(50) NOT NULL, City NVARCHAR(80) NOT NULL, CustomerSegment NVARCHAR(30) NOT NULL, CreatedDate DATE NOT NULL);
CREATE TABLE Products (ProductID INT PRIMARY KEY, ProductName NVARCHAR(120) NOT NULL UNIQUE, CategoryID INT NOT NULL FOREIGN KEY REFERENCES Categories(CategoryID), UnitCost DECIMAL(12,2) NOT NULL, UnitPrice DECIMAL(12,2) NOT NULL);
CREATE TABLE Orders (OrderID INT PRIMARY KEY, OrderDate DATE NOT NULL, CustomerID INT NOT NULL FOREIGN KEY REFERENCES Customers(CustomerID), Region NVARCHAR(50) NOT NULL, OrderStatus NVARCHAR(30) NOT NULL);
CREATE TABLE OrderItems (OrderItemID INT PRIMARY KEY, OrderID INT NOT NULL FOREIGN KEY REFERENCES Orders(OrderID), ProductID INT NOT NULL FOREIGN KEY REFERENCES Products(ProductID), Quantity INT NOT NULL CHECK (Quantity > 0), UnitPrice DECIMAL(12,2) NOT NULL, Discount DECIMAL(5,4) NOT NULL DEFAULT 0, UnitCost DECIMAL(12,2) NOT NULL);
CREATE INDEX IX_Orders_OrderDate ON Orders(OrderDate); CREATE INDEX IX_Orders_CustomerID ON Orders(CustomerID); CREATE INDEX IX_OrderItems_ProductID ON OrderItems(ProductID);

