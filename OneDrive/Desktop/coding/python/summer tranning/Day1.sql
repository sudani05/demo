/*
Commands:
DDL(Data Defination Language): create,alter, drop,truncate, rename
DML(Data Manipulate Language):insert, update, delete
DCL(Data Control Language): grant, revoke
TCL(Transaction Control Language):commit,rollback,saveprint
DQL(Data Query Language):select

Data types: int, float, char, varchar, date, boolean

*/

create database data_analysis_online2;
show databases;
use data_analysis_online2;
show tables;
create table pet(name varchar(20),owener varchar(20),species varchar(20),sex char(1),birth date,death date);
select * from pet;
select name,owener from pet;
insert into pet(name,owener,species,sex,birth,death) 
values('Whiskers','Carol','Cat','F','2021-01-12','2024-06-15'),('Rover','Dave','Dog','M','2019-01-01','2023-01-13'),('Fluffy','Alice','Cat','F','2022-09-07','2023-07-18');
update pet set sex='M' where name='Whiskers';
select * from pet where owener='Bob';
select * from pet where birth>='2024-06-01';
select * from pet where species='Cat' and sex='M';
select * from pet where (species='cat' and sex='M') or (species='dog' and sex='F');
select *from pet order by birth;
select *from pet order by age desc limit 1 offset 1;
select *,timestampdiff(year,birth,curdate())as age from pet order by age desc limit 1 offset 1;
drop table pet;
CREATE TABLE Employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    salary DECIMAL(10, 2),
    department VARCHAR(100),
    email_id VARCHAR(100),
    manager_name VARCHAR(100),
    manager_salary DECIMAL(10, 2)
);

INSERT INTO Employee (emp_id, emp_name, salary, department, email_id, manager_name, manager_salary) 
VALUES
    (1, 'John Doe', 50000.00, 'HR', 'john.doe@example.com', 'Michael Smith', 60000.00),
    (2, 'Jane Smith', 60000.00, 'Finance', 'jane.smith@com', 'Emily Johnson', 70000.00),
    (3, 'Alice Johnson', 55000.00, 'Marketing', 'alice.johnson@com', 'Michael Smith', 60000.00),
    (4, 'Bob Brown', 52000.00, 'IT', 'bob.brown@example.com', 'Emily Johnson', 70000.00),
    (5, 'Sam Wilson', 48000.00, 'HR', 'sam.wilson@example.com', 'Michael Smith', 60000.00),
    (6, 'Emily Johnson', 70000.00, 'Finance', 'emily.johnson@example.com', 'Michael Smith', 60000.00),
    (7, 'Michael Smith', 60000.00, 'IT', 'michael.smith@example.com', 'Emily Johnson', 70000.00),
    (8, 'Sarah Parker', 58000.00, 'Marketing', 'sarah.parker@example.com', 'Michael Smith', 60000.00),
    (9, 'David Davis', 53000.00, 'HR', 'david.davis@example.com', 'Michael Smith', 60000.00),
    (10, 'Laura Hill', 54000.00, 'Finance', 'laura.hill@example.com', 'Emily Johnson', 70000.00),
    (11, 'Mark Taylor', 51000.00, 'Marketing', 'mark.taylor@example.com', 'Michael Smith', 60000.00),
    (12, 'Julia White', 57000.00, 'IT', 'julia.white@com', 'Emily Johnson', 70000.00),
    (13, 'Ryan Lee', 49000.00, 'HR', 'ryan.lee@example.com', 'Michael Smith', 60000.00),
    (14, 'Chloe Adams', 62000.00, 'Finance', 'chloe.adams@example.com', 'Emily Johnson', 70000.00),
    (15, 'Eric Brown', 54000.00, 'IT', 'eric.brown@example.com', 'Emily Johnson', 70000.00),
    (16, 'Olivia Green', 56000.00, 'Marketing', 'olivia.green@example.com', 'Michael Smith', 60000.00),
    (17, 'Daniel Turner', 52000.00, 'HR', 'daniel.turner@example.com', 'Michael Smith', 60000.00),
    (18, 'Sophia King', 58000.00, 'Finance', 'sophia.king@example.com', 'Emily Johnson', 70000.00),
    (19, 'Jacob Evans', 51000.00, 'IT', 'jacob.evans@example.com', 'Emily Johnson', 70000.00),
    (20, 'Mia Carter', 53000.00, 'Marketing', 'mia.carter@example.com', 'Michael Smith', 60000.00);
    
    select * from employee where emp_name like 'm%';
    select * from employee where emp_name like '%son';
    select * from employee where emp_name like '%joh%';
    select * from employee where emp_name like '________';
    select * from employee where emp_name regexp 'son$nvct';
    select * from employee where emp_name regexp '^........$';
    
    select count(*) from employee;
    select department,count(*) from employee group by department;
    select manager_name,emp_name, count(*) as  count from employee  group by  manager_name,emp_name; 
     select manager_name, count(distinct department)as department_count from employee group by manager_name;
     
     show databases;
     use data_analysis_online2;
     create table students(student_id int primary key, name varchar(20),percentage  int);
     show tables;
     insert into students(student_id,name,percentage) values(3,'ranbir',76);
     
     select* from students;
     create table emp(emp_id int unique key,email_id varchar(30) unique key);
     insert into emp(emp_id,email_id) values (1,'smit@gmail.com'),(2,'raj@gmail.com');
     select * from emp;
     insert into emp(emp_id,email_id) values(3,null);
     insert into emp(emp_id,email_id) values(null,'sumit@gmail.com');
     
     create table sales(order_id int,product_id int,primary key(order_id,product_id));
     insert into sales(order_id,product_id) values (3,101),(4,404);
     select * from sales;
     
     create table orders(order_id int primary key,product_id int, customer_id int, foreign key (customer_id) reference emp(emp_id));
     
     select salary from employee where department='HR';
     select salary from employee where department ='it';
     
     
     create table project(emp_id int primary key, name varchar(20), project_assign varchar(20));

     insert into project(emp_id, name, project_assign) values (1, 'randhir', 'amazon'), (2, 'parag','zomato'), (3, 'rajvee', 'ola'), (4, 'ranbir', 'animal');

     create table HR(emp_id int primary key, salary int);
     insert into HR(emp_id, salary) values (1,10000000), (7,20000), (5,34200);
     
     select * from project;
     select project.emp_id,project.name,project. project_assign, HR.salary from project left join  HR on project.emp_id=HR.emp_id;
     
     
     select department  from employee;