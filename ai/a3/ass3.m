% Author: Hakon Mork
% I think this whole thing requires the Statistics toolbox.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%% Setup and initialization %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Flush out any garbage from last run
clc
clear
close all

% What to do.
% Use placemeans = true to place computed means (!)
% on top of the RGB image (for problem 1 and 2),
placemeans = false;

% Use segmenting = true to compute segmentations
% instead (for problem 3 and 4).
segmenting = false;

% Use gaussian3d to produce a 3d overlay of the
% computed weighted-average Gaussian on the input image.
gaussian3d = true;


% Read from image file into 20x20x3 matrix.
% Change the input file by hand!
rgbimg = imread('./images/image1_a.png', 'png');

% Reshape colors to 400x1 matrices
reds = reshape(rgbimg(:,:,1)', 400, 1);
greens = reshape(rgbimg(:,:,2)', 400, 1);
blues = reshape(rgbimg(:,:,3)', 400, 1);

% Vectors of x and y indices
xs = repmat((1:20)', 20, 1);
ys = [];
for i = 1:20
    ys = [ys; ones(20, 1) * i];
end

% Concatenate to 400x5 matrix of [r, g, b, x, y] values
rgbxy = [reds, greens, blues, xs, ys];
rgbxy = double(rgbxy);

% Number of clusters to divide the image into
clusters = 4;



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%% EM algorithm %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Construct initial guesses for means, covariances and
% weights for determining the impact of the initial parameters.

% These values are what the 'randSample' parameter give
% to gmdistribution.fit, but we need to construct
% them by hand to plot them with the convergence points.

% Pick random data points as initial means
randindex = randperm(length(rgbxy));
startmu = rgbxy(randindex(1:clusters),:);

% Initialize covariance matrices to variances of each component
startsigmas = eye(5);
for i = 1:clusters
    I = eye(5);
    I(I == 1) = var(rgbxy);
    startsigmas(:,:,i) = I;
end

% Assume equal weight for each gaussian
startweights = ones(clusters, 1) / clusters;

% EM argument structure
startstruct = struct('mu', startmu, ...
    'Sigma', startsigmas, ...
    'PComponents', startweights);

% Compute cluster gaussians, with or without
% a random initial guess of parameters, i.e. fit
% the data in rgbxy to a number of different clusters,
% starting with the initial guesses in startstruct.
obj = gmdistribution.fit(rgbxy, clusters, ...
    'Start', startstruct, ...
    'Regularize', 1e-7);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%% Visualization, problem 1 %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if placemeans
    % Initial and converged means for plotting
    meanx_init = startmu(:,4); % initial guess x-means
    meany_init = startmu(:,5); % initial guess y-means
    meanx_conv = obj.mu(:,4); % converged x-means
    meany_conv = obj.mu(:,5); % converged y-means
    
    
    % Display the rgb image itself as a backdrop
    imshow(rgbimg, ...
        'InitialMagnification', 2000, ...
        'Border', 'tight');
    
    % Put the convergeed mean x and y values on top of
    % the image as green dots, and the initial guesses
    % as green squares
    hold on
    scatter(meanx_init, meany_init, 100, 'gs', 'fill')
    scatter(meanx_conv, meany_conv, 100, 'go', 'fill')
    hold off
    
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%% Visualization, problem 3 %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if segmenting
    
    % Argmin mean of norm between data and means
    closest = 1:400;
    segmented = zeros(400, 3);
    for i = 1:400
        mindist = 1e300;
        for j = 1:clusters
            dist = norm(rgbxy(i,:) - obj.mu(j,:));
            if dist < mindist
                mindist = dist;
                closest(i) = j;
            end
        end
        segmented(i,:) = obj.mu(closest(i),1:3);
    end
    
    % Rounding
    segmented = uint8(segmented);
    
    rs = reshape(segmented(:,1), 20, 20)';
    gs = reshape(segmented(:,2), 20, 20)';
    bs = reshape(segmented(:,3), 20, 20)';
    
    % Concatenate in third dimension
    segrgb = cat(3, rs, gs, bs);
    
    % Save figure manually from popup window
    imshow(segrgb, ...
        'InitialMagnification', 2000, ...
        'Border', 'tight');
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%% Visualization for fancypants %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if gaussian3d
    
    % Draw 1000 samples according to the Gaussian distribution
    % we computed earlier. We'll use these data points to
    % make a new distribution object to plot.
    % It's a bit convoluted, but nevermind.
    samples = [];
    for k = 1:clusters
        sample_mu = [obj.mu(k,4), obj.mu(k,5)];
        sample_sigma = obj.Sigma(:,:,k);
        sample_sigma = sample_sigma(4:5, 4:5);
        samples = [samples; mvnrnd(sample_mu, sample_sigma, 1000)];
    end
    
    samples_xs = samples(:,1);
    samples_ys = samples(:,2);
    samples_obj = gmdistribution.fit(samples, clusters);
    
    range = [0, 20];
    funchandle = @(x, y) pdf(samples_obj, [x y]);
    
    % Plot 3d mesh grid with accompanying contour lines
    gaussianhandle = ezmeshc(funchandle, range, range);
    
    % Slight transparency because I'm being fancy
    set(gaussianhandle, 'FaceAlpha', 0.6);
    
    % We're not done placing stuff on the figure
    hold on
    
    % Z-level to place the contour on
    contourlevel = -0.005;
    
    % Set all the contour lines on the bottom of the
    % figure, instead of on z = 0.
    contourhandle = findobj('type', 'patch');
    zd = get(contourhandle, 'ZData');
    for i = 1:length(zd)
        set(contourhandle(i), 'ZData', ...
            contourlevel * ones(length(zd{i}), 1))
    end
    
    % We apparently need the transpose of the input image,
    % for some reason I'm not too clear on.
    disprgb(:,:,1) = rgbimg(:,:,1)';
    disprgb(:,:,2) = rgbimg(:,:,2)';
    disprgb(:,:,3) = rgbimg(:,:,3)';
    
    % Now, let's place the original image on the bottom of the
    % plot so we see how the Gaussian corresponds nicely
    % (hopefully) to the color blocks. We may have to run
    % it a couple of times to get nice results.
    
    % Got the idea for this part from StackOverflow,
    % http://stackoverflow.com/questions/3719502/how-can-i-plot-an-image-
    % jpg-in-matlab-in-both-2-d-and-3-d
    
    % The x data for the image corners
    xImage = [0 20; 0 20];
    % The y data for the image corners
    yImage = [0 0; 20 20];
    % The z data for the image corners
    zImage = [contourlevel, contourlevel; ...
        contourlevel, contourlevel];
    
    surf(xImage, yImage, zImage,...
        'CData', disprgb, ...
        'FaceColor', 'texturemap')
    
    title '' % Don't need a title
    
    axis([0, 20, 0, 20, contourlevel, 0.01])
    view([118, 20]) % Tilt so it's nicer to look at
    
end

