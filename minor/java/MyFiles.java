import java.io.*;

public class MyFiles {
    private File file;
    private String path = "MyFiles.txt";

    public static void main(String[] args) {
        MyFiles myFiles = new MyFiles();
        myFiles.createFile();
        myFiles.writeToFile("Hello, World!");
        myFiles.readFromFile();
        myFiles.appendToFile("Appending this line.");
        myFiles.readFromFile();
        myFiles.deleteFile();
    }


    public void createFile() {
        file = new File(path);
        try {
            if (file.createNewFile()) {
                System.out.println("File created: " + file.getName());
            } else {
                System.out.println("File already exists.");
            }
        } catch (IOException e) {
            System.out.println("Error creating file: " + e.getMessage());
        } finally {
            System.out.println("File path: " + file.getAbsolutePath());
        }
    }

    public void writeToFile(String content) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
            writer.write(content);
            writer.newLine();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("Error writing to file: " + e.getMessage());
        } finally {
            System.out.println("Content writen to file: " + content);
        }
    }

    public void readFromFile() {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            System.out.println("Reading from file: " + file.getName());
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.out.println("Error reading from file: "  + e.getMessage());
        } finally {
            System.out.println("Finished reading from file.");
        }
    }

    public void appendToFile(String content) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file, true))) {
            writer.write(content);
            writer.newLine();
            System.out.println("Successfully appended to the file.");
        } catch (IOException e) {
            System.out.println("Error appending to the file: " + e.getMessage());
        } finally {
            System.out.println("Content appended to file: " + content);
        }
    }

    public void deleteFile() {
        if (file.delete()) {
            System.out.println("Deleted the file: " + file.getName());
        } else {
            System.out.println("Failed to delete the file.");
        }
    }
}


