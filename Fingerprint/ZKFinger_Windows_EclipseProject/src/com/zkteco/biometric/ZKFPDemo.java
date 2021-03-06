package com.zkteco.biometric;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

import javax.imageio.ImageIO;
import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JRadioButton;
import javax.swing.JTextArea;

public class ZKFPDemo extends JFrame{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	JButton btnOpen = null;
	JButton btnEnroll = null;
	JButton btnVerify = null;
	JButton btnIdentify = null;
	JButton btnRegImg = null;
	JButton btnIdentImg = null;
	JButton btnClose = null;
	JButton btnImg = null;
	JRadioButton radioISO = null;
	JRadioButton radioANSI = null;
	JRadioButton radioZK = null;
	
	
	private JTextArea textArea;
	
	//the width of fingerprint image
	int fpWidth = 0;
	//the height of fingerprint image
	int fpHeight = 0;
	//for verify test
	private byte[] lastRegTemp = new byte[2048];
	//the length of lastRegTemp
	private int cbRegTemp = 0;
	//pre-register template
	private byte[][] regtemparray = new byte[3][2048];
	//Register
	private boolean bRegister = false;
	//Identify
	private boolean bIdentify = true;
	//finger id
	private int iFid = 1;
	
	private int nFakeFunOn = 1;
	//must be 3
	static final int enroll_cnt = 3;
	//the index of pre-register function
	private int enroll_idx = 0;
	
	private byte[] imgbuf = null;
	private byte[] template = new byte[2048];
	private int[] templateLen = new int[1];
	
	
	private boolean mbStop = true;
	private long mhDevice = 0;
	private long mhDB = 0;
	private WorkThread workThread = null;
	
	public void launchFrame(){
		this.setLayout (null);
		btnOpen = new JButton("Open");  
		this.add(btnOpen);  
		int nRsize = 20;
		btnOpen.setBounds(30, 10 + nRsize, 140, 30);
		
		btnEnroll = new JButton("Enroll");  
		this.add(btnEnroll);  
		btnEnroll.setBounds(30, 60 + nRsize, 140, 30);
		
		btnVerify = new JButton("Verify");  
		this.add(btnVerify);  
		btnVerify.setBounds(30, 110 + nRsize, 140, 30);
		
		btnIdentify = new JButton("Identify");  
		this.add(btnIdentify);  
		btnIdentify.setBounds(30, 160 + nRsize, 140, 30);
		
		btnRegImg = new JButton("Register By Image");  
		this.add(btnRegImg);  
		btnRegImg.setBounds(30, 210 + nRsize, 140, 30);
		
		btnIdentImg = new JButton("Verify By Image");  
		this.add(btnIdentImg);  
		btnIdentImg.setBounds(30, 260 + nRsize, 140, 30);
		
		
		btnClose = new JButton("Close");  
		this.add(btnClose);  
		btnClose.setBounds(30, 310 + nRsize, 140, 30);
		
		
		//For ISO/Ansi/ZK
		radioANSI = new JRadioButton("ANSI", true);
		this.add(radioANSI);  
		radioANSI.setBounds(30, 360 + nRsize, 60, 30);
		
		radioISO = new JRadioButton("ISO");
		this.add(radioISO);  
		radioISO.setBounds(120, 360 + nRsize, 60, 30);
		
		radioZK = new JRadioButton("ZK");
		this.add(radioZK);
		radioZK.setBounds(210, 360 + nRsize, 60, 30);
        
        ButtonGroup group = new ButtonGroup();
        group = new ButtonGroup();
        group.add(radioANSI);
        group.add(radioISO);
        group.add(radioZK);
        //For End
        
		btnImg = new JButton();
		btnImg.setBounds(200, 5, 288, 375);
		btnImg.setDefaultCapable(false);
		this.add(btnImg); 
		
		textArea = new JTextArea();
		this.add(textArea);  
		textArea.setBounds(10, 420, 490, 150);
		textArea.setLineWrap(true);
		textArea.setSelectedTextColor(Color.RED);
		
		this.setSize(520, 620);
		this.setLocationRelativeTo(null);
		this.setVisible(true);
		this.setTitle("ZKFingerSDK Demo");
		this.setResizable(false);
		
		btnOpen.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				if (0 != mhDevice)
				{
					//already inited
					textArea.setText("Please close device first!\n");
					return;
				}
				int ret = FingerprintSensorErrorCode.ZKFP_ERR_OK;
				//Initialize
				cbRegTemp = 0;
				bRegister = false;
				bIdentify = false;
				iFid = 1;
				enroll_idx = 0;
				if (FingerprintSensorErrorCode.ZKFP_ERR_OK != FingerprintSensorEx.Init())
				{
					textArea.setText("Init failed!\n");
					return;
				}
				ret = FingerprintSensorEx.GetDeviceCount();
				if (ret < 0)
				{
					textArea.setText("No devices connected!\n");
					FreeSensor();
					return;
				}
				if (0 == (mhDevice = FingerprintSensorEx.OpenDevice(0)))
				{
					textArea.setText("Open device fail, ret = " + ret + "!\n");
					FreeSensor();
					return;
				}
				if (0 == (mhDB = FingerprintSensorEx.DBInit()))
				{
					textArea.setText("Init DB fail, ret = " + ret + "!\n");
					FreeSensor();
					return;
				}
				
				//For ISO/Ansi
				int nFmt = 0;	//Ansi
				if (radioISO.isSelected())
				{
					nFmt = 1;	//ISO
				}
				FingerprintSensorEx.DBSetParameter(mhDB,  5010, nFmt);				
				//For ISO/Ansi End
				
				//set fakefun off
				//FingerprintSensorEx.SetParameter(mhDevice, 2002, changeByte(nFakeFunOn), 4);
				
				byte[] paramValue = new byte[4];
				int[] size = new int[1];
				//GetFakeOn
				//size[0] = 4;
				//FingerprintSensorEx.GetParameters(mhDevice, 2002, paramValue, size);
				//nFakeFunOn = byteArrayToInt(paramValue);
				
				size[0] = 4;
				FingerprintSensorEx.GetParameters(mhDevice, 1, paramValue, size);
				fpWidth = byteArrayToInt(paramValue);
				size[0] = 4;
				FingerprintSensorEx.GetParameters(mhDevice, 2, paramValue, size);
				fpHeight = byteArrayToInt(paramValue);
								
				imgbuf = new byte[fpWidth*fpHeight];
				//btnImg.resize(fpWidth, fpHeight);
				mbStop = false;
				workThread = new WorkThread();
			    workThread.start();// ????????????
				textArea.setText("Open succ! Finger Image Width:" + fpWidth + ",Height:" + fpHeight +"\n");
			}
		});
		
		
		
		btnClose.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				FreeSensor();
				
				textArea.setText("Close succ!\n");
			}
		});
		
		btnEnroll.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				if(0 == mhDevice)
				{
					textArea.setText("Please Open device first!\n");
					return;
				}
				if(!bRegister)
				{
					enroll_idx = 0;
					bRegister = true;
					textArea.setText("Please your finger 3 times!\n");
				}
			}
			});
		
		btnVerify.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				if(0 == mhDevice)
				{
					textArea.setText("Please Open device first!\n");
					return;
				}
				if(bRegister)
				{
					enroll_idx = 0;
					bRegister = false;
				}
				if(bIdentify)
				{
					bIdentify = false;
				}
			}
			});
		
		btnIdentify.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				if(0 == mhDevice)
				{
					textArea.setText("Please Open device first!\n");
					return;
				}
				if(bRegister)
				{
					enroll_idx = 0;
					bRegister = false;
				}
				if(!bIdentify)
				{
					bIdentify = true;
				}
			}
			});
		
		
		btnRegImg.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				if(0 == mhDB)
				{
					textArea.setText("Please open device first!\n");
				}
				String path = "d:\\test\\fingerprint.bmp";
				byte[] fpTemplate = new byte[2048];
				int[] sizeFPTemp = new int[1];
				sizeFPTemp[0] = 2048;
				int ret = FingerprintSensorEx.ExtractFromImage( mhDB, path, 500, fpTemplate, sizeFPTemp);		
				if (0 == ret)
				{
					ret = FingerprintSensorEx.DBAdd( mhDB, iFid, fpTemplate);
					if (0 == ret)
					{
						//String base64 = fingerprintSensor.BlobToBase64(fpTemplate, sizeFPTemp[0]);		
						iFid++;
                    	cbRegTemp = sizeFPTemp[0];
                        System.arraycopy(fpTemplate, 0, lastRegTemp, 0, cbRegTemp);
                        //Base64 Template
                        //String strBase64 = Base64.encodeToString(regTemp, 0, ret, Base64.NO_WRAP);
                        textArea.setText("enroll succ\n");
					}
					else
					{
						textArea.setText("DBAdd fail, ret=" + ret + "\n");
					}
				}
				else
				{
					textArea.setText("ExtractFromImage fail, ret=" + ret + "\n");
				}
			}
			});
		
		
		btnIdentImg.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				if(0 ==  mhDB)
				{
					textArea.setText("Please open device first!\n");
				}
				String path = "d:\\test\\fingerprint.bmp";
				byte[] fpTemplate = new byte[2048];
				int[] sizeFPTemp = new int[1];
				sizeFPTemp[0] = 2048;
				int ret = FingerprintSensorEx.ExtractFromImage(mhDB, path, 500, fpTemplate, sizeFPTemp);
				if (0 == ret)
				{
					if (bIdentify)
					{
						int[] fid = new int[1];
						int[] score = new int [1];
						ret = FingerprintSensorEx.DBIdentify(mhDB, fpTemplate, fid, score);
                        if (ret == 0)
                        {
                        	textArea.setText("Identify succ, fid=" + fid[0] + ",score=" + score[0] + "\n");
                        }
                        else
                        {
                        	textArea.setText("Identify fail, errcode=" + ret +"\n");
                        }
                            
					}
					else
					{
						if(cbRegTemp <= 0)
						{
							textArea.setText("Please register first!\n");
						}
						else
						{
							ret = FingerprintSensorEx.DBMatch(mhDB, lastRegTemp, fpTemplate);
							if(ret > 0)
							{
								textArea.setText("Verify succ, score=" + ret + "\n");
							}
							else
							{
								textArea.setText("Verify fail, ret=" + ret +"\n");
							}
						}
					}
				}
				else
				{
					textArea.setText("ExtractFromImage fail, ret=" + ret + "\n");
				}
			}
		});
	
		
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.addWindowListener(new WindowAdapter(){

            @Override
            public void windowClosing(WindowEvent e) {
                // TODO Auto-generated method stub
            	FreeSensor();
            }
		});
	}
	
	private void FreeSensor()
	{
		mbStop = true;
		try {		//wait for thread stopping
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		if (0 != mhDB)
		{
			FingerprintSensorEx.DBFree(mhDB);
			mhDB = 0;
		}
		if (0 != mhDevice)
		{
			FingerprintSensorEx.CloseDevice(mhDevice);
			mhDevice = 0;
		}
		FingerprintSensorEx.Terminate();
	}
	
	public static void writeBitmap(byte[] imageBuf, int nWidth, int nHeight,
			String path) throws IOException {
		java.io.FileOutputStream fos = new java.io.FileOutputStream(path);
		java.io.DataOutputStream dos = new java.io.DataOutputStream(fos);

		int w = (((nWidth+3)/4)*4);
		int bfType = 0x424d; // ?????????????????????0???1?????????
		int bfSize = 54 + 1024 + w * nHeight;// bmp??????????????????2???5?????????
		int bfReserved1 = 0;// ?????????????????????????????????0???6-7?????????
		int bfReserved2 = 0;// ?????????????????????????????????0???8-9?????????
		int bfOffBits = 54 + 1024;// ??????????????????????????????????????????????????????????????????10-13?????????

		dos.writeShort(bfType); // ????????????????????????'BM'
		dos.write(changeByte(bfSize), 0, 4); // ????????????????????????
		dos.write(changeByte(bfReserved1), 0, 2);// ???????????????????????????
		dos.write(changeByte(bfReserved2), 0, 2);// ???????????????????????????
		dos.write(changeByte(bfOffBits), 0, 4);// ???????????????????????????

		int biSize = 40;// ??????????????????????????????14-17?????????
		int biWidth = nWidth;// ???????????????18-21?????????
		int biHeight = nHeight;// ???????????????22-25?????????
		int biPlanes = 1; // ?????????????????????????????????1???26-27?????????
		int biBitcount = 8;// ??????????????????????????????28-29?????????????????????1??????????????????4??????16?????????8??????256????????????24???????????????????????????
		int biCompression = 0;// ??????????????????????????????0??????????????????30-33????????????1???BI_RLEB??????????????????2???BI_RLE4????????????????????????
		int biSizeImage = w * nHeight;// ?????????????????????????????????????????????????????????????????????34-37?????????
		int biXPelsPerMeter = 0;// ??????????????????????????????????????????38-41????????????????????????????????????
		int biYPelsPerMeter = 0;// ??????????????????????????????????????????42-45????????????????????????????????????
		int biClrUsed = 0;// ????????????????????????????????????????????????46-49?????????????????????0??????????????????????????????
		int biClrImportant = 0;// ???????????????????????????????????????(50-53??????)????????????0???????????????????????????

		dos.write(changeByte(biSize), 0, 4);// ????????????????????????????????????
		dos.write(changeByte(biWidth), 0, 4);// ??????????????????
		dos.write(changeByte(biHeight), 0, 4);// ??????????????????
		dos.write(changeByte(biPlanes), 0, 2);// ?????????????????????????????????
		dos.write(changeByte(biBitcount), 0, 2);// ????????????????????????????????????
		dos.write(changeByte(biCompression), 0, 4);// ???????????????????????????
		dos.write(changeByte(biSizeImage), 0, 4);// ???????????????????????????
		dos.write(changeByte(biXPelsPerMeter), 0, 4);// ??????????????????????????????
		dos.write(changeByte(biYPelsPerMeter), 0, 4);// ??????????????????????????????
		dos.write(changeByte(biClrUsed), 0, 4);// ?????????????????????????????????
		dos.write(changeByte(biClrImportant), 0, 4);// ?????????????????????????????????????????????

		for (int i = 0; i < 256; i++) {
			dos.writeByte(i);
			dos.writeByte(i);
			dos.writeByte(i);
			dos.writeByte(0);
		}

		byte[] filter = null;
		if (w > nWidth)
		{
			filter = new byte[w-nWidth];
		}
		
		for(int i=0;i<nHeight;i++)
		{
			dos.write(imageBuf, (nHeight-1-i)*nWidth, nWidth);
			if (w > nWidth)
				dos.write(filter, 0, w-nWidth);
		}
		dos.flush();
		dos.close();
		fos.close();
	}

	public static byte[] changeByte(int data) {
		return intToByteArray(data);
	}
	
	public static byte[] intToByteArray (final int number) {
		byte[] abyte = new byte[4];  
	    // "&" ??????AND??????????????????????????????????????????????????????????????????????????????1?????????1?????????0???  
	    abyte[0] = (byte) (0xff & number);  
	    // ">>"????????????????????????????????????0???????????????????????????1  
	    abyte[1] = (byte) ((0xff00 & number) >> 8);  
	    abyte[2] = (byte) ((0xff0000 & number) >> 16);  
	    abyte[3] = (byte) ((0xff000000 & number) >> 24);  
	    return abyte; 
	}	 
		 
		public static int byteArrayToInt(byte[] bytes) {
			int number = bytes[0] & 0xFF;  
		    // "|="??????????????????  
		    number |= ((bytes[1] << 8) & 0xFF00);  
		    number |= ((bytes[2] << 16) & 0xFF0000);  
		    number |= ((bytes[3] << 24) & 0xFF000000);  
		    return number;  
		 }
	
		private class WorkThread extends Thread {
	        @Override
	        public void run() {
	            super.run();
	            int ret = 0;
	            while (!mbStop) {
	            	templateLen[0] = 2048;
	            	if (0 == (ret = FingerprintSensorEx.AcquireFingerprint(mhDevice, imgbuf, template, templateLen)))
	            	{
	            		if (nFakeFunOn == 1)
                    	{
                    		byte[] paramValue = new byte[4];
            				int[] size = new int[1];
            				size[0] = 4;
            				int nFakeStatus = 0;
            				//GetFakeStatus
            				ret = FingerprintSensorEx.GetParameters(mhDevice, 2004, paramValue, size);
            				nFakeStatus = byteArrayToInt(paramValue);
            				System.out.println("ret = "+ ret +",nFakeStatus=" + nFakeStatus);
            				if (0 == ret && (byte)(nFakeStatus & 31) != 31)
            				{
            					textArea.setText("Is a fake finger?\n");
            					return;
            				}
                    	}
                    	OnCatpureOK(imgbuf);
                    	OnExtractOK(template, templateLen[0]);
	            	}
	                try {
	                    Thread.sleep(500);
	                } catch (InterruptedException e) {
	                    e.printStackTrace();
	                }

	            }
	        }
	    }
		
		private void OnCatpureOK(byte[] imgBuf)
		{
			try {
				writeBitmap(imgBuf, fpWidth, fpHeight, "fingerprint.bmp");
				btnImg.setIcon(new ImageIcon(ImageIO.read(new File("fingerprint.bmp"))));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		private void OnExtractOK(byte[] template, int len)
		{
			if(bRegister)
			{
				int[] fid = new int[1];
				int[] score = new int [1];
                int ret = FingerprintSensorEx.DBIdentify(mhDB, template, fid, score);
                if (ret == 0)
                {
                    textArea.setText("the finger already enroll by " + fid[0] + ",cancel enroll\n");
                    bRegister = false;
                    enroll_idx = 0;
                    return;
                }
                if (enroll_idx > 0 && FingerprintSensorEx.DBMatch(mhDB, regtemparray[enroll_idx-1], template) <= 0)
                {
                	textArea.setText("please press the same finger 3 times for the enrollment\n");
                    return;
                }
                System.arraycopy(template, 0, regtemparray[enroll_idx], 0, 2048);
                enroll_idx++;
                if (enroll_idx == 3) {
                	int[] _retLen = new int[1];
                    _retLen[0] = 2048;
                    byte[] regTemp = new byte[_retLen[0]];
                    
                    if (0 == (ret = FingerprintSensorEx.DBMerge(mhDB, regtemparray[0], regtemparray[1], regtemparray[2], regTemp, _retLen)) &&
                    		0 == (ret = FingerprintSensorEx.DBAdd(mhDB, iFid, regTemp))) {
                    	iFid++;
                    	cbRegTemp = _retLen[0];
                        System.arraycopy(regTemp, 0, lastRegTemp, 0, cbRegTemp);
                        //Base64 Template
                        textArea.setText("enroll succ:\n");
                        try {
							File file = new File("saved_fingerprint.fp");
							// Initialize a pointer
							// in file using OutputStream
							OutputStream
								os
								= new FileOutputStream(file);
				  
							// Starts writing the bytes in it
							os.write(regTemp);
							System.out.println("Successfully"
											   + " byte inserted");
							int s = regTemp.length;
							System.out.println(s);
				  
							// Close the file
							os.close();
						}
				  
						catch (Exception e) {
							System.out.println("Exception: " + e);
						}
                    } else {
                    	textArea.setText("enroll fail, error code=" + ret + "\n");
                    }
                    bRegister = false;
                } else {
                	textArea.setText("You need to press the " + (3 - enroll_idx) + " times fingerprint\n");
                }
			}
			else
			{
				if (bIdentify)
				{
					int[] fid = new int[1];
					int[] score = new int [1];
					int ret = FingerprintSensorEx.DBIdentify(mhDB, template, fid, score);
                    if (ret == 0)
                    {
                    	textArea.setText("Identify succ, fid=" + fid[0] + ",score=" + score[0] +"\n");
                    }
                    else
                    {
                    	textArea.setText("Identify fail, errcode=" + ret + "\n");
                    }
                        
				}
				else
				{
					if(cbRegTemp <= 0)
					{
						textArea.setText("Please register first!\n");
					}
					else
					{
						int ret = FingerprintSensorEx.DBMatch(mhDB, lastRegTemp, template);
						if(ret > 0)
						{
							textArea.setText("Verify succ, score=" + ret + "\n");
						}
						else
						{
							textArea.setText("Verify fail, ret=" + ret + "\n");
						}
					}
				}
			}
		}
		
		public static void main(String[] args) {
			new ZKFPDemo().launchFrame();
		}
}
