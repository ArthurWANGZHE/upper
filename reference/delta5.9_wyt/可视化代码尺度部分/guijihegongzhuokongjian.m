%运行后暂停即可，忘记代码是干什么的了，便于观察？
clc;
clear;
close all;
rng(0); % 设置随机数生成器的种子为0
R1 = 202;%静平台的外接圆半径
R2 = 50;%动平台的外接圆半径
R = R1-R2;%三角锥法后移动到一点后的向xoy投影的三角形的半径
x1 = [R1, -R1/2, -R1/2];
y1 = [0, -sqrt(3)*R1/2, sqrt(3)*R1/2];
z1 = [-500, -500, -500];

% 第二组点的坐标
x2 = [R1, -R1/2, -R1/2];
y2 = [0, -sqrt(3)*R1/2, sqrt(3)*R1/2];
z2 = [0, 0, 0];

% 第三组点的坐标
x3 = [R1,R1];
y3 = [0,0];
z3 = [0, -500];

x4 = [-R1/2, -R1/2];
y4 = [-sqrt(3)*R1/2, -sqrt(3)*R1/2];
z4 = [0, -500];

x5 = [-R1/2, -R1/2];
y5 = [sqrt(3)*R1/2, sqrt(3)*R1/2];
z5 = [0, -500];

x6 = [R1, -R1/2];
y6 = [0, sqrt(3)*R1/2];
z6 = [-500, -500];

x7 = [R1, -R1/2];
y7 = [0, sqrt(3)*R1/2];
z7 = [0, 0];

% 绘制线段
plot3(x1, y1, z1, 'b', 'LineWidth', 2);
hold on;
plot3(x2, y2, z2, 'r', 'LineWidth', 2);
plot3(x3, y3, z3, 'g', 'LineWidth', 2);
plot3(x4, y4, z4, 'g', 'LineWidth', 2);
plot3(x5, y5, z5, 'g', 'LineWidth', 2);
plot3(x6, y6, z6, 'b', 'LineWidth', 2);
plot3(x7, y7, z7, 'r', 'LineWidth', 2);

% 设置坐标轴标签
xlabel('X');
ylabel('Y');
zlabel('Z');

% 设置图形标题
title('可视化正解与轨迹');

% 添加网格线
grid on;

for i =1:0.5:1000
t1 = randi([0, 250]); % 假设值
t2 = randi([0, 250]); % 假设值
t3 = randi([0, 250]); % 假设值
% t1=250;
% t2=0;
% t3=0;
%想起来是干什么的了，就是这个改了改jy代码，也算可以正解吧。注释for循环输入t1，t2，t3就行，
% t1，t2，t3可以输入数组，这个jy、该好了，丢进去方便看。
% 定义OB, OC, OD
plot3(R1, 0, -t1, 'go', 'MarkerSize', 10);
plot3(-R1/2, -sqrt(3)*R1/2, -t2, 'go', 'MarkerSize', 10);
plot3(-R1/2, sqrt(3)*R1/2, -t3, 'go', 'MarkerSize', 10);

% 定义点的坐标
point1 = [R1, 0, -t1];
point2 = [-R1/2, -sqrt(3)*R1/2, -t2];
point3 = [-R1/2, sqrt(3)*R1/2, -t3];

OB = [-R*cos(30*pi/180), R*sin(30*pi/180), -t2];
OC = [R*cos(30*pi/180), R*sin(30*pi/180), -t1];
OD = [0, -R, -t3];


% 定义AB为杆长
AB = 300;

% 计算向量BC和CD
BC = OC - OB;
CD = OD - OC;
BD = OD -OB;
% 计算OE
OE = (OB + OC) / 2;

% 计算BE
lbe = norm(BC) / 2;

% 计算nef，即BC和CD的叉积的叉积
BCCD =cross(BC,CD);
nef = cross(BCCD, BC)/norm(BCCD)/norm(BC);

% 计算a, b, c（注意这里将角度转换为弧度）
a = sqrt((t3 - t2)^2 + (sqrt(3) * R)^2);
b = sqrt((t2 - t1)^2 + (sqrt(3) * R)^2);
c = sqrt((t3 - t1)^2 + (sqrt(3) * R)^2);

% 计算p和S
p = (a + b + c) / 2;
S = sqrt(p * (p - a) * (p - b) * (p - c));

% 这里BF似乎是一个错误，应该是lbf
lbf = a * b * c / (4 * S);

% 计算Lef
Lef = sqrt(lbf^2 - lbe^2);

% 计算EF
EF = Lef * nef;

% 这里似乎有一个错误，应该是Lfa而不是BF
Lfa = sqrt(AB^2 - lbf^2);

% 计算nfa
nfa = cross(BC, CD)/norm(BCCD);

% 计算FA
FA = Lfa * nfa;

% 计算OF
OF = OE + EF;

% 计算OA
OA = OF + FA;

% 提取x, y, z坐标
x = OA(1);
y = OA(2);
z = OA(3);
disp(['x = ', num2str(x)]);
disp(['y = ', num2str(y)]);
disp(['z = ', num2str(z)]);
plot3(x, y, z, 'b.'); % 使用蓝色点表示茄子的位置
hold on; % 保持图形，以便绘制下一个茄子的位置
% 绘制连接point1、dian的线段
% 提取x, y, z坐标
x = OA(1);
y = OA(2);
z = OA(3);

% 存储茄子位置的坐标
dian = [x, y, z];

% 绘制茄子位置点
plot3(x, y, z, 'bo', 'MarkerSize', 2);

    
hold on; % 保持图形，以便绘制下一个茄子的位置

end
xlabel('x'); % x轴标签
ylabel('y'); % y轴标签
zlabel('z'); % z轴标签
grid on; % 显示网格
axis square; % 设置坐标轴比例为等比例
