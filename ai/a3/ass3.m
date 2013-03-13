% clear previous context
clc
clear

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%% reading and preparing input %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% read from file into 20x20x3 matrix
rgbimg = imread('./images/image1_a.png', 'png');

% reshape colors to 400x1 matrices
reds = reshape(rgbimg(:,:,1)', 400, 1);
greens = reshape(rgbimg(:,:,2)', 400, 1);
blues = reshape(rgbimg(:,:,3)', 400, 1);

% x and y indices
xs = repmat((1:20)', 20, 1);
ys = [];
for i = 1:20
    ys = [ys; ones(20, 1) * i];
end

% concatenate to 400x5 matrix of [r, g, b, x, y] values
rgbxy = [reds, greens, blues, xs, ys];
rgbxy = double(rgbxy);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%% setting up EM %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% number of clusters/gaussians
clusters = 4;

% 5 values for each data point: r, g, b, x, y
datapoints = 5;

% 5-by-#clusters matrix of means: rgbxy mean values for each cluster
%mus = rand(datapoints, clusters);
% multiply by 20 so we spread them out across the image
mus = rand(datapoints, clusters) * 20;
%mus(:,1)
mus(1:3,:) = 255;

% covariance matrices, one for each gaussian
sigmas = [];
for i = 1:clusters
    % we need a 2x2 symmetric positive definite matrix
    % any matrix multiplied by its transpose has this property
    m = randn(datapoints);
    newsigma = m' * m;
    % we multiply it by some number,
    % so it doesn't get so sharp and thin
    sigmas(:,:,i) = newsigma * 10;
end

% weight parameters
weights = ones(clusters, 1);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%% EM algorithm itself %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
iterations = 0;
converged = false;
while ~converged
    
    for i = 1:clusters
        
        %%%%%%% setup %%%%%%%
        
        mu = mus(:,i);
        sigma = sigmas(:,:,i);
        
        % normalization constant
        alpha = 1;
        
        
        %%%%%%% e step %%%%%%%
        
        % probabilities of this distribution at each sample
        p_ijs = zeros(length(rgbxy), 1);
        
        % make all the p_ij values
        for j = 1:length(rgbxy)
            % get the datapoint x_j on the right format
            x_j = rgbxy(i,:)';
            % probability at x of the i-th gaussian
            % i.e., P(x_j | C = i)
            % using multivariate normal distribution
            p_ijs(i) = mvnpdf(x_j, mu, sigma);
        end
        
        % adjust with normalization and weight parameters
        % p_ij = alpha * P(x_j | C = i) * P(C = i)
        %      = alpha * P(x_j | C = i) * w_i
        p_ijs = alpha * p_ijs * weights(i);
        p_ijs
        
        % sum of all probabilities for this gaussian
        p_i = sum(p_ijs);
        
        
        %%%%%%% m step %%%%%%%
        
        newmu = 0;
        newsigma = zeros(datapoints); % 5x5
        for j = 1:length(p_ijs)
            x_j = rgbxy(j,:);
            p_ij = p_ijs(j);
            newmu = newmu + (p_ij * x_j) / p_i;
            newsigma = newsigma + (p_ij * x_j' * x_j) / p_i;
        end        
        
        % update for next iteration
        mus(:,i) = newmu;
        sigmas(:,:,i) = newsigma;
        weights(i) = p_i;
        
    end
    
    iterations = iterations + 1;
    converged = true;
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%% result visualization %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% % bounds and grid
% lower = 1;
% upper = 20;
% res = 0.2;
% [x, y] = meshgrid(lower:res:upper, lower:res:upper);
%
% % add up all the distributions
% f = 0;
% for i = 1:clusters
%     mu = mus(:, i);
%     sigma = sigmas(:,:,i);
%     % multivariate normal distribution
%     % with the given mean and covariance matrices
%     g = mvnpdf([x(:), y(:)], mu, sigma);
%     % reshape to square
%     g = reshape(g, length(y), length(x));
%     % and add to the final value
%     f = f + g;
% end
%
% %contour(x, y, f)
% surf(x, y, f)

sprintf('done')

