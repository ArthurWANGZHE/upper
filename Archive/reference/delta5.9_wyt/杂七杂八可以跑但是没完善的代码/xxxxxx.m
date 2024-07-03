% 定义门型轨迹的控制点，感觉双s应该用于圆弧过度部分。
% 这里只画了个门型轨迹，不大妥。然后代码还没改完
points = [-25, 0, 0; -25, 0, 25; 100, 0, 25; 100, 0, 0];

% 计算轨迹长度
trajectory_length = size(points, 1);

% 初始化轨迹参数
trajectory_params = struct('Ta', [], 'Td', [], 'Tv', [], 'T', [], 'vmax', [], 'amax', []);

% 定义机器人参数
vmax = 15; % 最大速度
amax = 10; % 最大加速度

% 初始化起始速度和位置
q0 = 0;
v0 = 0;

% 计算每段轨迹的时间参数
for i = 1:(trajectory_length - 1)
    % 计算段的长度
    segment_length = norm(points(i + 1, :) - points(i, :));
    
    % 计算时间参数
    Ta = vmax / amax; % 加速阶段时间
    Td = vmax / amax; % 减速阶段时间
    Tv = (segment_length / vmax) - (Ta + Td); % 匀速阶段时间
    T = Ta + Tv + Td; % 总时间
    
    % 存储时间参数
    trajectory_params(i).Ta = Ta;
    trajectory_params(i).Td = Td;
    trajectory_params(i).Tv = Tv;
    trajectory_params(i).T = T;
    trajectory_params(i).vmax = vmax;
    trajectory_params(i).amax = amax;
end

% 初始化绘图
figure;
hold on;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('门型轨迹');

% 绘制控制点
plot3(points(:,1), points(:,2), points(:,3), 'ro-', 'LineWidth', 2);

% 初始化轨迹点
trajectory_points = [];

% 逐段应用双S型运动规律并计算轨迹
for i = 1:(trajectory_length - 1)
    % 获取时间参数
    Ta = trajectory_params(i).Ta;
    Td = trajectory_params(i).Td;
    Tv = trajectory_params(i).Tv;
    T = trajectory_params(i).T;
    vmax = trajectory_params(i).vmax;
    amax = trajectory_params(i).amax;
    
    % 应用双S型运动规律计算轨迹参数
    t = 0:0.1:T;
    p_segment = [];
    
    for t_i = t
        if t_i <= Ta
            % 加速阶段
            q = q0 + v0 * t_i + 0.5 * amax * t_i^2;
        elseif t_i <= (T - Td)
            % 匀速阶段
            q = q0 + v0 * Ta + vmax * (t_i - Ta);
        else
            % 减速阶段
            q = q0 + v0 * Ta + vmax * Tv + v0 * (t_i - T) - 0.5 * amax * (t_i - T)^2;
        end
        
        p_segment = [p_segment; q];
    end
    
    % 将当前段的轨迹连接到总轨迹
    trajectory_points = [trajectory_points; p_segment];
end

% 绘制轨迹
plot3(trajectory_points(:,1), trajectory_points(:,2), trajectory_points(:,3), 'b-', 'LineWidth', 2);

% 设置图形属性
axis equal;
grid on;
view(3);

% 绘制动态轨迹
for i = 1:size(trajectory_points, 1)
    plot3(trajectory_points(i,1), trajectory_points(i,2), trajectory_points(i,3), 'bo', 'MarkerSize', 5);
    drawnow;
    pause(0.05);
end
