%b样条门型路径规划及离散，命令窗口里有插值点坐标
close all;
clear;
clc;

% 定义控制点
cpts = [-25, 0, 0; -25, 0, 25; 0, 0, 50; 75, 0, 50; 100, 0, 25; 100, 0, 0];

% 定义时间点
tpts = [0, 5];

% 定义时间向量
tvec = 0:0.01:5;

% 生成随机B样条轨迹（这里仅为示例）
[q, ~, ~, ~] = bsplinepolytraj(cpts', tpts, tvec); % 注意这里对cpts进行转置

% 绘制
figure;
plot3(cpts(:, 1), cpts(:, 2), cpts(:, 3), 'm-', 'LineWidth', 1);
hold on;
plot3(q(1,:), q(2,:), q(3,:), 'LineWidth', 2, 'color', 'b');
grid on;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('B样条轨迹优化');
hold on
% 对生成的轨迹点进行离散并计算插值点坐标
t_interp = 0:0.05:5; % 新的时间向量，以0.1为步长离散

% 对 x、y、z 分别进行插值
x_interp = interp1(tvec, q(1,:), t_interp);
y_interp = interp1(tvec, q(2,:), t_interp);
z_interp = interp1(tvec, q(3,:), t_interp);

% 将插值后的坐标放入一个数组中
interp_points = [x_interp', y_interp', z_interp'];

% 绘制插值后的轨迹点
figure;
plot3(interp_points(:,1), interp_points(:,2), interp_points(:,3), 'o', 'LineWidth', 2, 'MarkerSize', 5, 'MarkerFaceColor', 'c');
hold on;
plot3(cpts(:, 1), cpts(:, 2), cpts(:, 3), '*', 'LineWidth', 5);
grid on;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('B样条轨迹优化（插值后）');
legend('插值点', '控制点');
hold off;

% 输出插值点坐标
disp('插值点坐标：');
disp(interp_points);
