import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.canvas.*;
import javafx.scene.layout.Pane;
import javafx.animation.Timeline;
import javafx.animation.KeyFrame;
import javafx.util.Duration;
import java.util.ArrayList;
import javafx.scene.paint.Color;

public class SnakeGameidk extends Application {
    private static final int WIDTH = 400;
    private static final int HEIGHT = 400;
    private static final int BLOCK_SIZE = 20;
    private ArrayList<int[]> snake = new ArrayList<>();
    private int[] food = new int[2];
    private String direction = "RIGHT";
    private boolean gameOver = false;

    @Override
    public void start(Stage primaryStage) {
        Pane root = new Pane();
        Canvas canvas = new Canvas(WIDTH, HEIGHT);
        root.getChildren().add(canvas);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        // Initialize snake and food
        snake.add(new int[]{5, 5});
        spawnFood();

        // Game loop
        Timeline timeline = new Timeline(new KeyFrame(Duration.millis(100), e -> {
            if (!gameOver) {
                updateGame();
                drawGame(gc);
            }
        }));
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();

        // Keyboard input
        Scene scene = new Scene(root, WIDTH, HEIGHT);
        scene.setOnKeyPressed(event -> {
            switch (event.getCode()) {
                case UP: if (!direction.equals("DOWN")) direction = "UP"; break;
                case DOWN: if (!direction.equals("UP")) direction = "DOWN"; break;
                case LEFT: if (!direction.equals("RIGHT")) direction = "LEFT"; break;
                case RIGHT: if (!direction.equals("LEFT")) direction = "RIGHT"; break;
            }
        });

        primaryStage.setTitle("Snake Game");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void updateGame() {
        int[] head = snake.get(0).clone();
        switch (direction) {
            case "UP": head[1]--; break;
            case "DOWN": head[1]++; break;
            case "LEFT": head[0]--; break;
            case "RIGHT": head[0]++; break;
        }

        // Check collision with walls
        if (head[0] < 0 || head[0] >= WIDTH / BLOCK_SIZE || 
            head[1] < 0 || head[1] >= HEIGHT / BLOCK_SIZE) {
            gameOver = true;
            return;
        }

        // Check collision with self
        for (int[] segment : snake) {
            if (head[0] == segment[0] && head[1] == segment[1]) {
                gameOver = true;
                return;
            }
        }

        snake.add(0, head);
        if (head[0] == food[0] && head[1] == food[1]) {
            spawnFood();
        } else {
            snake.remove(snake.size() - 1);
        }
    }

    private void spawnFood() {
        food[0] = (int) (Math.random() * (WIDTH / BLOCK_SIZE));
        food[1] = (int) (Math.random() * (HEIGHT / BLOCK_SIZE));
    }

    private void drawGame(GraphicsContext gc) {
        gc.setFill(Color.BLACK);
        gc.fillRect(0, 0, WIDTH, HEIGHT);

        gc.setFill(Color.GREEN);
        for (int[] segment : snake) {
            gc.fillRect(segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        }

        gc.setFill(Color.RED);
        gc.fillRect(food[0] * BLOCK_SIZE, food[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);

        if (gameOver) {
            gc.setFill(Color.WHITE);
            gc.fillText("Game Over", WIDTH / 2 - 30, HEIGHT / 2);
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}