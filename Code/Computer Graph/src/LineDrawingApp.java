import javax.swing.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.event.MouseMotionAdapter;

public class LineDrawingApp extends JFrame {
    private JComboBox<String> algorithmComboBox;
    private JComboBox<String> shapeComboBox;
    private JTextField x1Field;
    private JTextField y1Field;
    private JTextField x2Field;
    private JTextField y2Field;
    private JTextField centerXField;
    private JTextField centerYField;
    private JTextField radiusXField;
    private JTextField radiusYField;
    private JButton drawButton;
    private DrawPanel drawPanel;
    private JLabel statusBar;

    public LineDrawingApp() {
        super("Line Drawing - DDA & Midpoint (Bresenham)");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // 美化：系统外观
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignore) {}

        JPanel controlPanel = new JPanel(new GridBagLayout());
        controlPanel.setBorder(new TitledBorder("控制面板"));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(4, 4, 4, 4);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        algorithmComboBox = new JComboBox<>(new String[]{"DDA", "中点", "Bresenham"});
        shapeComboBox = new JComboBox<>(new String[]{"直线", "椭圆"});
        x1Field = new JTextField("10", 8);
        y1Field = new JTextField("10", 8);
        x2Field = new JTextField("200", 8);
        y2Field = new JTextField("120", 8);
        centerXField = new JTextField("100", 8);
        centerYField = new JTextField("100", 8);
        radiusXField = new JTextField("80", 8);
        radiusYField = new JTextField("60", 8);
        drawButton = new JButton("绘制");
        JButton clearButton = new JButton("清空");

        int row = 0;
        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("图形:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(shapeComboBox, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("算法:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(algorithmComboBox, gbc); row++;

        // 直线参数
        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("x1:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(x1Field, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("y1:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(y1Field, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("x2:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(x2Field, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("y2:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(y2Field, gbc); row++;

        // 椭圆参数
        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("中心X:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(centerXField, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("中心Y:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(centerYField, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("半径X:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(radiusXField, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; controlPanel.add(new JLabel("半径Y:"), gbc);
        gbc.gridx = 1; gbc.gridy = row; controlPanel.add(radiusYField, gbc); row++;

        gbc.gridx = 0; gbc.gridy = row; gbc.gridwidth = 2; controlPanel.add(drawButton, gbc); row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.gridwidth = 2; controlPanel.add(clearButton, gbc);

        add(controlPanel, BorderLayout.WEST);

        drawPanel = new DrawPanel();
        drawPanel.setPreferredSize(new Dimension(800, 600));
        add(drawPanel, BorderLayout.CENTER);

        // 状态栏
        statusBar = new JLabel(" 坐标: ");
        JPanel statusPanel = new JPanel(new BorderLayout());
        statusPanel.add(statusBar, BorderLayout.WEST);
        add(statusPanel, BorderLayout.SOUTH);

        drawButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                onDrawClicked();
            }
        });

        clearButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                drawPanel.clearAll();
            }
        });

        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    private void onDrawClicked() {
        try {
            String shape = (String) shapeComboBox.getSelectedItem();
            String algo = (String) algorithmComboBox.getSelectedItem();
            
            if ("直线".equals(shape)) {
                int x1 = Integer.parseInt(x1Field.getText().trim());
                int y1 = Integer.parseInt(y1Field.getText().trim());
                int x2 = Integer.parseInt(x2Field.getText().trim());
                int y2 = Integer.parseInt(y2Field.getText().trim());

                if ("DDA".equals(algo)) {
                    drawPanel.setLine(new LineSpec(x1, y1, x2, y2, LineSpec.Algorithm.DDA));
                } else if ("中点".equals(algo)) {
                    drawPanel.setLine(new LineSpec(x1, y1, x2, y2, LineSpec.Algorithm.MIDPOINT));
                } else if ("Bresenham".equals(algo)) {
                    drawPanel.setLine(new LineSpec(x1, y1, x2, y2, LineSpec.Algorithm.BRESENHAM));
                }
            } else if ("椭圆".equals(shape)) {
                int centerX = Integer.parseInt(centerXField.getText().trim());
                int centerY = Integer.parseInt(centerYField.getText().trim());
                int radiusX = Integer.parseInt(radiusXField.getText().trim());
                int radiusY = Integer.parseInt(radiusYField.getText().trim());

                if ("Bresenham".equals(algo)) {
                    drawPanel.setLine(new LineSpec(centerX, centerY, radiusX, radiusY, LineSpec.Algorithm.BRESENHAM, LineSpec.Shape.ELLIPSE));
                } else {
                    JOptionPane.showMessageDialog(this, "椭圆绘制仅支持Bresenham算法", "提示", JOptionPane.INFORMATION_MESSAGE);
                }
            }
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "请输入有效的整数坐标", "输入错误", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new LineDrawingApp();
            }
        });
    }

    private static class LineSpec {
        enum Algorithm { DDA, MIDPOINT, BRESENHAM }
        enum Shape { LINE, ELLIPSE }
        final int x1, y1, x2, y2;
        final int centerX, centerY, radiusX, radiusY;
        final Algorithm algorithm;
        final Shape shape;

        // 直线构造函数
        LineSpec(int x1, int y1, int x2, int y2, Algorithm algorithm) {
            this.x1 = x1;
            this.y1 = y1;
            this.x2 = x2;
            this.y2 = y2;
            this.algorithm = algorithm;
            this.shape = Shape.LINE;
            this.centerX = 0;
            this.centerY = 0;
            this.radiusX = 0;
            this.radiusY = 0;
        }

        // 椭圆构造函数
        LineSpec(int centerX, int centerY, int radiusX, int radiusY, Algorithm algorithm, Shape shape) {
            this.centerX = centerX;
            this.centerY = centerY;
            this.radiusX = radiusX;
            this.radiusY = radiusY;
            this.algorithm = algorithm;
            this.shape = shape;
            this.x1 = 0;
            this.y1 = 0;
            this.x2 = 0;
            this.y2 = 0;
        }
    }

    private class DrawPanel extends JPanel {
        private LineSpec lineSpec;
        private Point firstPoint;
        private Point secondPoint;
        private double scale = 1.0; // 缩放比例（世界单位 -> 屏幕像素）
        private double translateX = 0.0; // 屏幕平移（像素）
        private double translateY = 0.0; // 屏幕平移（像素），正值使世界上移（屏幕Y减小）
        private Point lastDragPoint = null; // 中键拖拽

        // 坐标变换：世界 -> 屏幕
        private int worldToScreenX(double wx) {
            return (int) Math.round(wx * scale + translateX);
        }
        private int worldToScreenY(double wy) {
            return (int) Math.round(getHeight() - (wy * scale + translateY));
        }
        // 坐标变换：屏幕 -> 世界
        private double screenToWorldX(int sx) {
            return (sx - translateX) / scale;
        }
        private double screenToWorldY(int sy) {
            return ((getHeight() - sy) - translateY) / scale;
        }

        void setLine(LineSpec spec) {
            this.lineSpec = spec;
            repaint();
        }

        void clearAll() {
            this.lineSpec = null;
            this.firstPoint = null;
            this.secondPoint = null;
            repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);

            // draw axes/grid for reference（以左下角为原点的世界坐标系）
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            // world grid step（世界单位）
            double gridStepWorld = niceGridStep();
            double minWorldX = screenToWorldX(0);
            double maxWorldX = screenToWorldX(getWidth());
            double minWorldY = screenToWorldY(getHeight());
            double maxWorldY = screenToWorldY(0);

            // 对齐到网格
            double startX = Math.floor(minWorldX / gridStepWorld) * gridStepWorld;
            double startY = Math.floor(minWorldY / gridStepWorld) * gridStepWorld;

            // 画网格
            g2.setColor(new Color(240, 240, 240));
            for (double x = startX; x <= maxWorldX; x += gridStepWorld) {
                int sx = worldToScreenX(x);
                g2.drawLine(sx, 0, sx, getHeight());
            }
            for (double y = startY; y <= maxWorldY; y += gridStepWorld) {
                int sy = worldToScreenY(y);
                g2.drawLine(0, sy, getWidth(), sy);
            }

            // 画坐标轴（x=0, y=0）
            g2.setColor(new Color(180, 180, 180));
            g2.setStroke(new BasicStroke(2f));
            int axisX = worldToScreenX(0);
            int axisY = worldToScreenY(0);
            g2.drawLine(0, axisY, getWidth(), axisY);
            g2.drawLine(axisX, 0, axisX, getHeight());

            // 刻度与标签（世界单位）
            g2.setFont(g2.getFont().deriveFont(11f));
            g2.setStroke(new BasicStroke(1f));
            g2.setColor(new Color(150, 150, 150));
            for (double x = startX; x <= maxWorldX; x += gridStepWorld) {
                int sx = worldToScreenX(x);
                g2.drawLine(sx, axisY - 4, sx, axisY + 4);
                if (Math.abs(x) > 1e-9) g2.drawString(Integer.toString((int) Math.round(x)), sx + 2, axisY - 6);
            }
            for (double y = startY; y <= maxWorldY; y += gridStepWorld) {
                int sy = worldToScreenY(y);
                g2.drawLine(axisX - 4, sy, axisX + 4, sy);
                if (Math.abs(y) > 1e-9) g2.drawString(Integer.toString((int) Math.round(y)), axisX + 6, sy - 2);
            }

            if (lineSpec == null) return;

            if (lineSpec.shape == LineSpec.Shape.LINE) {
                if (lineSpec.algorithm == LineSpec.Algorithm.DDA) {
                    drawLineDDA(g2, worldToScreenX(lineSpec.x1), worldToScreenY(lineSpec.y1), worldToScreenX(lineSpec.x2), worldToScreenY(lineSpec.y2));
                } else if (lineSpec.algorithm == LineSpec.Algorithm.MIDPOINT) {
                    drawLineMidpoint(g2, worldToScreenX(lineSpec.x1), worldToScreenY(lineSpec.y1), worldToScreenX(lineSpec.x2), worldToScreenY(lineSpec.y2));
                } else if (lineSpec.algorithm == LineSpec.Algorithm.BRESENHAM) {
                    drawLineBresenham(g2, worldToScreenX(lineSpec.x1), worldToScreenY(lineSpec.y1), worldToScreenX(lineSpec.x2), worldToScreenY(lineSpec.y2));
                }
            } else if (lineSpec.shape == LineSpec.Shape.ELLIPSE) {
                if (lineSpec.algorithm == LineSpec.Algorithm.BRESENHAM) {
                    drawEllipseBresenham(g2, worldToScreenX(lineSpec.centerX), worldToScreenY(lineSpec.centerY), 
                                       (int)(lineSpec.radiusX * scale), (int)(lineSpec.radiusY * scale));
                }
            }

            // highlight selected points if present
            if (firstPoint != null) drawPointMarker(g2, new Point(worldToScreenX(firstPoint.x), worldToScreenY(firstPoint.y)), Color.MAGENTA);
            if (secondPoint != null) drawPointMarker(g2, new Point(worldToScreenX(secondPoint.x), worldToScreenY(secondPoint.y)), Color.ORANGE);
        }

        private void putPixel(Graphics2D g2, int x, int y) {
            g2.fillRect(x, y, 1, 1);
        }

        private void drawPointMarker(Graphics2D g2, Point p, Color color) {
            Color old = g2.getColor();
            g2.setColor(color);
            int r = 3;
            g2.fillOval(p.x - r, p.y - r, r * 2, r * 2);
            g2.setColor(old);
        }

         //1. DDA算法
        private void drawLineDDA(Graphics2D g2, int x1, int y1, int x2, int y2) {
            g2.setColor(Color.BLUE);
            int dx = x2 - x1;
            int dy = y2 - y1;

            int steps = Math.max(Math.abs(dx), Math.abs(dy));
            double xInc = dx / (double) steps;
            double yInc = dy / (double) steps;

            double x = x1;
            double y = y1;
            for (int i = 0; i <= steps; i++) {
                putPixel(g2, (int) Math.round(x), (int) Math.round(y));
                x += xInc;
                y += yInc;
            }
        }

        //2. 中点算法
        private void drawLineMidpoint(Graphics2D g2, int x1, int y1, int x2, int y2) {
            g2.setColor(Color.RED);

            int dx = Math.abs(x2 - x1);
            int dy = Math.abs(y2 - y1);
            int sx = x1 < x2 ? 1 : -1;
            int sy = y1 < y2 ? 1 : -1;

            boolean steep = dy > dx;
            if (steep) {
                // swap x/y
                int tmp;
                tmp = x1; x1 = y1; y1 = tmp;
                tmp = x2; x2 = y2; y2 = tmp;
                dx = Math.abs(x2 - x1);
                dy = Math.abs(y2 - y1);
                sx = x1 < x2 ? 1 : -1;
                sy = y1 < y2 ? 1 : -1;
            }

            int d = 2 * dy - dx;
            int y = y1;
            for (int x = x1; x != x2 + sx; x += sx) {
                if (steep) putPixel(g2, y, x); else putPixel(g2, x, y);
                if (d > 0) {
                    y += sy;
                    d -= 2 * dx;
                }
                d += 2 * dy;
            }
        }

        //3. Bresenham算法
        private void drawLineBresenham(Graphics2D g2, int x1, int y1, int x2, int y2) {
            g2.setColor(Color.GREEN);
            
            int dx = Math.abs(x2 - x1);
            int dy = Math.abs(y2 - y1);
            int sx = x1 < x2 ? 1 : -1;
            int sy = y1 < y2 ? 1 : -1;
            int err = dx - dy;
            
            int x = x1;
            int y = y1;
            
            while (true) {
                putPixel(g2, x, y);
                
                if (x == x2 && y == y2) break;
                
                int e2 = 2 * err;
                if (e2 > -dy) {
                    err -= dy;
                    x += sx;
                }
                if (e2 < dx) {
                    err += dx;
                    y += sy;
                }
            }
        }

        //4. Bresenham椭圆算法
        private void drawEllipseBresenham(Graphics2D g2, int centerX, int centerY, int radiusX, int radiusY) {
            g2.setColor(new Color(128, 0, 128)); // 紫色
            
            int x = 0;
            int y = radiusY;
            int radiusX2 = radiusX * radiusX;
            int radiusY2 = radiusY * radiusY;
            int twoRadiusX2 = 2 * radiusX2;
            int twoRadiusY2 = 2 * radiusY2;
            int p;
            int px = 0;
            int py = twoRadiusX2 * radiusY;
            
            // 绘制第一象限的椭圆弧
            drawEllipsePoints(g2, centerX, centerY, x, y);
            
            // 区域1：斜率 < 1
            p = (int) Math.round(radiusY2 - (radiusX2 * radiusY) + (0.25 * radiusX2));
            while (px < py) {
                x++;
                px += twoRadiusY2;
                if (p < 0) {
                    p += radiusY2 + px;
                } else {
                    y--;
                    py -= twoRadiusX2;
                    p += radiusY2 + px - py;
                }
                drawEllipsePoints(g2, centerX, centerY, x, y);
            }
            
            // 区域2：斜率 >= 1
            p = (int) Math.round(radiusY2 * (x + 0.5) * (x + 0.5) + radiusX2 * (y - 1) * (y - 1) - radiusX2 * radiusY2);
            while (y > 0) {
                y--;
                py -= twoRadiusX2;
                if (p > 0) {
                    p += radiusX2 - py;
                } else {
                    x++;
                    px += twoRadiusY2;
                    p += radiusX2 - py + px;
                }
                drawEllipsePoints(g2, centerX, centerY, x, y);
            }
        }
        
        private void drawEllipsePoints(Graphics2D g2, int centerX, int centerY, int x, int y) {
            // 绘制椭圆的四个对称点
            putPixel(g2, centerX + x, centerY + y);
            putPixel(g2, centerX - x, centerY + y);
            putPixel(g2, centerX + x, centerY - y);
            putPixel(g2, centerX - x, centerY - y);
        }

        {
            // 初始化鼠标监听（实例初始化块）
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    if (!isEnabled()) return;
                    // 右键清空
                    if (SwingUtilities.isRightMouseButton(e)) {
                        clearAll();
                        return;
                    }
                    Point clickedScreen = e.getPoint();
                    int wx = (int) Math.round(screenToWorldX(clickedScreen.x));
                    int wy = (int) Math.round(screenToWorldY(clickedScreen.y));
                    if (firstPoint == null) {
                        firstPoint = new Point(wx, wy);
                        // 同步输入框 x1,y1
                        x1Field.setText(Integer.toString(wx));
                        y1Field.setText(Integer.toString(wy));
                    } else if (secondPoint == null) {
                        secondPoint = new Point(wx, wy);
                        // 同步输入框 x2,y2
                        x2Field.setText(Integer.toString(wx));
                        y2Field.setText(Integer.toString(wy));
                        // 两点齐备，按当前算法绘制
                        String shape = (String) shapeComboBox.getSelectedItem();
                        String algo = (String) algorithmComboBox.getSelectedItem();
                        
                        if ("直线".equals(shape)) {
                            if ("DDA".equals(algo)) {
                                setLine(new LineSpec(firstPoint.x, firstPoint.y, secondPoint.x, secondPoint.y, LineSpec.Algorithm.DDA));
                            } else if ("中点".equals(algo)) {
                                setLine(new LineSpec(firstPoint.x, firstPoint.y, secondPoint.x, secondPoint.y, LineSpec.Algorithm.MIDPOINT));
                            } else if ("Bresenham".equals(algo)) {
                                setLine(new LineSpec(firstPoint.x, firstPoint.y, secondPoint.x, secondPoint.y, LineSpec.Algorithm.BRESENHAM));
                            }
                        } else if ("椭圆".equals(shape)) {
                            // 对于椭圆，使用第一个点作为中心，第二个点计算半径
                            int radiusX = Math.abs(secondPoint.x - firstPoint.x);
                            int radiusY = Math.abs(secondPoint.y - firstPoint.y);
                            if ("Bresenham".equals(algo)) {
                                setLine(new LineSpec(firstPoint.x, firstPoint.y, radiusX, radiusY, LineSpec.Algorithm.BRESENHAM, LineSpec.Shape.ELLIPSE));
                            }
                        }
                    } else {
                        // 第三次左键点击：从头开始选点
                        firstPoint = new Point(wx, wy);
                        secondPoint = null;
                        x1Field.setText(Integer.toString(wx));
                        y1Field.setText(Integer.toString(wy));
                        repaint();
                    }
                    repaint();
                }
            });

            // 中键拖拽平移
            addMouseMotionListener(new MouseMotionAdapter() {
                @Override
                public void mouseDragged(MouseEvent e) {
                    if (SwingUtilities.isMiddleMouseButton(e)) {
                        if (lastDragPoint == null) {
                            lastDragPoint = e.getPoint();
                            return;
                        }
                        Point p = e.getPoint();
                        int dx = p.x - lastDragPoint.x;
                        int dy = p.y - lastDragPoint.y;
                        translateX += dx;
                        translateY -= dy;
                        lastDragPoint = p;
                        repaint();
                    }
                }

                @Override
                public void mouseMoved(MouseEvent e) {
                    double wx = screenToWorldX(e.getX());
                    double wy = screenToWorldY(e.getY());
                    statusBar.setText(" 坐标: (" + String.format("%.2f", wx) + ", " + String.format("%.2f", wy) + ")  缩放: " + String.format("%.2f", scale));
                }
            });

            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseReleased(MouseEvent e) {
                    lastDragPoint = null;
                }
            });

            // 滚轮缩放（以鼠标为中心）
            addMouseWheelListener(new MouseWheelListener() {
                @Override
                public void mouseWheelMoved(MouseWheelEvent e) {
                    int notches = e.getWheelRotation();
                    double factor = Math.pow(1.1, -notches);
                    if ((scale * factor) < 0.1) return;
                    if ((scale * factor) > 50) return;
                    // 缩放前鼠标对应的世界坐标
                    double wx = screenToWorldX(e.getX());
                    double wy = screenToWorldY(e.getY());
                    scale *= factor;
                    // 调整平移，使缩放围绕鼠标位置
                    translateX = e.getX() - wx * scale;
                    translateY = (getHeight() - e.getY()) - wy * scale;
                    repaint();
                }
            });
        }

        private double niceGridStep() {
            // 使屏幕上网格间距大约为 50~120 像素
            double[] candidates = {1, 2, 5, 10, 20, 50, 100, 200, 500};
            double targetPixels = 80.0;
            double best = 10;
            double bestDiff = Double.MAX_VALUE;
            for (double c : candidates) {
                double pixels = c * scale;
                double diff = Math.abs(pixels - targetPixels);
                if (diff < bestDiff) {
                    bestDiff = diff;
                    best = c;
                }
            }
            return best;
        }
    }
}


