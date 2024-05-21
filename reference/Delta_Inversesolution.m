function [x,y,z] = Delta_Inversesolution(t1,t2,t3)


R1 = 125;%静平台的外接圆半径
R2 = 60;%动平台的外接圆半径
R = R1-R2;%三角锥法后移动到一点后的向xoy投影的三角形的半径

OB = [-R*cos(30*pi/180), R*sin(30*pi/180), -t2];
OC = [R*cos(30*pi/180), R*sin(30*pi/180), -t1];
OD = [0, -R, -t3];
OB2 = [-R*cos(30*pi/180), R*sin(30*pi/180), 0];
OC2 = [R*cos(30*pi/180), R*sin(30*pi/180), 0];
OD2 = [0, -R, 0];
E =[0,0,-1];%垂直的单位向量
pmB = cross(E,OB2);%面法线
pmC = cross(E,OC2);%面法线
pmD = cross(E,OD2);%面法线
% 定义AB为杆长
AB = 280;

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


Lfa = sqrt(AB^2 - lbf^2);

% 计算nfa
nfa = cross(BC, CD)/norm(BCCD);

% 计算FA
FA = Lfa * nfa;

% 计算OF
OF = OE + EF;

% 计算OA
OA = OF + FA;
AB = OB-OA;
AC = OC-OA;
AD = OD-OA;
cosbb = dot(pmB,AB)/(norm(pmB)*norm(AB));%角度值
coscc = dot(pmC,AC)/(norm(pmC)*norm(AC));%角度值
cosdd = dot(pmD,AD)/(norm(pmD)*norm(AD));%角度值
% 提取x, y, z坐标
x = OA(1);
y = OA(2);
z = OA(3);
end