% %空间直线-圆弧插补法和3-4-5次多项式运动规律
clear; clc; close all

% 门型点
P1 = [-150; -50; -400];  % 第一个门型点的坐标
P2 = [-150; 25; -400];    % 第二个门型点的坐标
P3 = [-150+75; 100; -400];   % 第三个门型点的坐标
P4 = [-75+150; 100; -400];   % 第四个门型点的坐标
P5 = [150; 25; -400];     % 第五个门型点的坐标
P6 = [150; -50; -400];    % 第六个门型点的坐标

P = [P1 P2 P3 P4 P5 P6];   % 将所有门型点组合成一个矩阵

% 计算第1段长度 - 直线
s1=sqrt(sum((P2-P1).^2));
% 计算第2段长度 - 圆弧
s2=2*pi*sqrt(sum((P3(1)-P2(1)).^2))/4;
% 计算第3段长度 - 直线
s3=sqrt(sum((P4-P3).^2));
% 计算第4段长度 - 圆弧
s4=2*pi*sqrt(sum((P5(1)-P4(1)).^2))/4;
% 计算第5段长度 - 直线
s5=sqrt(sum((P6-P5).^2));

% 计算总路径长度
s12345=s1+s2+s3+s4+s5;

% 设定最大加速度
amax=20;
% 计算运动总时间
T=sqrt(8.135*s12345/amax);
% 初始化加速度、速度、位置、时间等数组
svajArr=[];
tArr=[];
tNorm=[];
pArr=[];
mydt=0.1; % 时间步长
for t=0:mydt:T
    % 计算当前时间占总时间的比例
    tao=t/T;
    % 根据时间比例计算当前位置、速度、加速度和 加加速度
    s=amax/8.135*T*T*(20*tao^3-45*tao^4+36*tao^5-10*tao^6);
    v=amax/8.135*T*(60*tao^2-180*tao^3+180*tao^4-60*tao^5);
    a=amax/8.135*(120*tao-540*tao^2+720*tao^3-300*tao^4);
    j=amax/8.135/T*(120-1080*tao+2160*tao^2-1200*tao^3);
    % 将计算结果保存到数组中
    svajArr=[svajArr;s,v,a,j];
    tArr=[tArr;t];
    % 根据当前位置选择对应的门型点
    if s<=s1
        scal=s/s1;
        p=P1+(P2-P1)*scal;
        pArr=[pArr;p'];
    elseif s<=(s1+s2)
        scal=(s-s1)/s2;
        r=sqrt(sum((P3(1)-P2(1)).^2));
        p=P2+r*[cos(pi-scal*pi/2)+1;sin(pi-scal*pi/2);0];
        pArr=[pArr;p'];
    elseif s<=(s1+s2+s3)
        scal=(s-s1-s2)/s3;
        p=P3+(P4-P3)*scal;
        pArr=[pArr;p'];
    elseif s<=(s1+s2+s3+s4)
        scal=(s-s1-s2-s3)/s4;
        r=sqrt(sum((P5(1)-P4(1)).^2));
        p=P4+r*[cos(pi/2-scal*pi/2);sin(pi/2-scal*pi/2)-1;0];
        pArr=[pArr;p'];
    else
        scal=(s-s1-s2-s3-s4)/s5;
        p=P5+(P6-P5)*scal;
        pArr=[pArr;p'];
    end
end

% 计算最大速度
S=amax/8.135*T*T;
% 绘制速度、加速度、J、JJ随时间的变化图像
figure('Name', '运动参数变化', 'NumberTitle', 'off');
for i=1:4
    subplot(2,2,i)
    plot(tArr,svajArr(:,i))
    switch i
        case 1
            title('速度随与时间关系')
            ylabel('速度')
        case 2
            title('加速度与时间关系')
            ylabel('加速度')
        case 3
            title('加加速度与时间关系')
            ylabel('加加速度')
        case 4
            title('加加加速度与时间关系')
            ylabel('加加加速度')
    end
    xlabel('时间')
end
% 计算路径上每个时间点的位置
p=pArr;

% 创建新的 3D 图形窗口
figure('Name', '插值得到的点坐标');

% 绘制插值得到的点
scatter3(p(:,1), p(:,2), p(:,3), 10, 'o', 'filled'); 
hold on;
grid on;
axis equal;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('插值得到的点集合即离散路径');


% 创建新的 3D 图形窗口
figure('Name', '门型路径', 'NumberTitle', 'off');

% 绘制门型路径的图
scatter3(P(1,:),P(2,:),P(3,:), 'filled');
hold on;
plot3(p(:,1),p(:,2),p(:,3), 'm', 'linewidth', 2);
grid on;
axis equal;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('原始点集及门型路径');

% 显示图例
legend('门型路径', '点');
