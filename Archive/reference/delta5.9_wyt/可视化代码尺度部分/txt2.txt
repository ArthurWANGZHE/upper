%随机生成的点以及对应的t1，t2，t3过程，可看命令窗口
clc;
clear;
close all;
rng(0); % 设置随机数生成器的种子为0
R1 = 202; % 静平台的外接圆半径
R2 = 50; % 动平台的外接圆半径
R = R1 - R2; % 三角锥法后移动到一点后的向xoy投影的三角形的半径
l = 300; % 杆长

% 设置坐标轴标签和图形标题
xlabel('X');
ylabel('Y');
zlabel('Z');
title('可视化反解与轨迹');

for i = 1:0.1:5000
    % 随机生成 x、y、z
    x = randi([-150, 150]);
    y = randi([-150, 150]);
    z = randi([-500, -250]);
    
    % 计算 t1、t2、t3
    t3 = -z - sqrt(l^2 - x^2 - (y + R1)^2);
    t2 = -z - sqrt(l^2 - (x - sqrt(3)/2 * R1)^2 - (R1/2 - y)^2);
    t1 = -z - sqrt(l^2 - (sqrt(3)/2 * R1 + x)^2 - (R1/2 - y)^2);
    
    % 检查 t1、t2、t3 是否在指定范围内
    if t1 >= 0 && t1 <= 250 && t2 >= 0 && t2 <= 250 && t3 >= 0 && t3 <= 250
        % 输出 x、y、z
        disp(['x = ', num2str(x)]);
        disp(['y = ', num2str(y)]);
        disp(['z = ', num2str(z)]);
        
        % 输出 t1、t2、t3
        disp(['t1 = ', num2str(t1)]);
        disp(['t2 = ', num2str(t2)]);
        disp(['t3 = ', num2str(t3)]);
        
        % 绘制茄子的位置点
        plot3(x, y, z, 'b.', 'MarkerSize', 10);
        hold on
        
        % 绘制 t1、t2、t3 对应的点
        plot3(R1, 0, -t1, 'go', 'MarkerSize', 10);
        plot3(-R1/2, -sqrt(3)*R1/2, -t2, 'go', 'MarkerSize', 10);
        plot3(-R1/2, sqrt(3)*R1/2, -t3, 'go', 'MarkerSize', 10);
    end
    
    % 等待一段时间，方便观察
    pause(0.1);
end


 % 设置图形属性
    xlabel('x'); % x轴标签
    ylabel('y'); % y轴标签
    zlabel('z'); % z轴标签
    grid on; % 显示网格
    axis square; % 设置坐标轴比例为等比例
    drawnow;