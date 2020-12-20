import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Menu extends JFrame {

    JPanel contents = new JPanel(new FlowLayout());
    JPanel selectionPanel = new JPanel();
    JPanel croppingPanel = new JPanel();
    JPanel scalePanel = new JPanel();
    JPanel processPanel = new JPanel();
    JPanel imagePanel = new ImagePanel("");
    JPanel p = new JPanel();
    JTextArea pL = new JTextArea("", 22, 10);

    JButton selectImageButton, croppingButton, scaleButton, processButton;
    JTextField scaleField;
    JLabel scaleLabelNM;
    String calculatedScale = "\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|";
    double scaleValue;

    // specify file for object detection algorithm
    private static final String CMD_COMMAND = "python_exec_file.py";

    public Menu(String title) {
        super(title);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        selectImageButton = new JButton("Select image");
        selectImageButton.setPreferredSize(new Dimension(120, 40));

        selectionPanel.add(selectImageButton);
        contents.add(selectionPanel);

        croppingButton = new JButton("Cropping");
        croppingButton.setPreferredSize(new Dimension(120, 40));
        croppingButton.setEnabled(false);
        croppingPanel.add(croppingButton);
        contents.add(croppingPanel);


        scaleButton = new JButton("Scale");
        scaleButton.setPreferredSize(new Dimension(120, 40));
        scaleButton.setEnabled(false);
        scaleField = new JTextField();
        scaleField.setPreferredSize(new Dimension(50, 25));
        scaleField.setEnabled(false);
        scaleLabelNM = new JLabel("nm");
        scalePanel.add(scaleButton);
        scalePanel.add(scaleField);
        scalePanel.add(scaleLabelNM);
        contents.add(scalePanel);

        processButton = new JButton("Process");
        processButton.setPreferredSize(new Dimension(120, 40));
        processButton.setEnabled(false);
        processPanel.add(processButton);
        contents.add(processPanel);

        contents.add(imagePanel);


        pL.setMinimumSize(new Dimension(600, 35));
        pL.setVisible(false);
        p.add(pL);
        contents.add(pL);

        eMenuHandler handler = new eMenuHandler(this);
        selectImageButton.addActionListener(handler);
        scaleButton.addActionListener(handler);
        processButton.addActionListener(handler);
        setContentPane(contents);
    }

    public class eMenuHandler implements ActionListener {

        Menu menu;
        public eMenuHandler() {
        }

        public eMenuHandler(Menu menu) {
            this.menu = menu;
        }

        @Override
        public void actionPerformed(ActionEvent event) {

            if (event.getSource() == selectImageButton) {
                FileDialog dialog = new FileDialog(new JFrame(), "Choose a file", FileDialog.LOAD);
                dialog.setVisible(true);
                imagePanel.removeAll();
                String image = dialog.getFile();
                JLabel label = new JLabel();

                try {
                    label.setIcon(new ImageIcon(ImageIO.read(new File(dialog.getDirectory() + image))));
                } catch (IOException e) {
                    e.printStackTrace();
                }
                if (image == null || image.isEmpty()) {
                    return;
                }
                imagePanel.add(label);
                imagePanel.updateUI();
                scaleButton.setEnabled(true);
                scaleField.setEnabled(true);
                processButton.setEnabled(true);
                pL.setVisible(false);
                pL.setEnabled(false);
                pL.setDisabledTextColor(Color.blue);
            }

            if (event.getSource() == croppingButton) {

            }

            if (event.getSource() == scaleButton) {
                if (!scaleField.getText().isEmpty()) {
                    try {
                        scaleValue = Double.valueOf(scaleField.getText());
                        if (scaleValue <= 0) {
                            return;
                        }
                        pL.setVisible(true);
                        pL.setText("| " + scaleValue + calculatedScale);
                    } catch (NumberFormatException nfe) {
                        nfe.printStackTrace();
                    }
                }
            }

            if (event.getSource() == processButton) {
                ProcessBuilder processBuilder = new ProcessBuilder();
                processBuilder.command("cmd.exe", "/c", CMD_COMMAND);
                try {
                    Process process = processBuilder.start();
                    JOptionPane.showMessageDialog(menu, "status: finished", "info", JOptionPane.INFORMATION_MESSAGE, null);
                } catch (IOException ioe) {
                    ioe.printStackTrace();
                }
            }
        }

    }


    public class ImagePanel extends JPanel{

        private BufferedImage image;

        public ImagePanel(String path) {
            try {
                image = ImageIO.read(new File(path));
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.drawImage(image, 0, 0, this);
        }

    }
}
