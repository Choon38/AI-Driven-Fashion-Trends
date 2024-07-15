package ijaux.moments.zernike;

import java.util.ArrayList;

import ij.IJ;
import ij.ImagePlus;
import ij.process.ImageProcessor;
import ijaux.datatype.ComplexArray;
import static java.lang.Math.*;

public class ZernikeMoment {
	int degree;
	int centerX;
	int centerY;
	double radius;
	// eliminate RadialValue
	//public RadialValue[] rv=null;
	public RadialValue[] rv=null;
	public ZernikeMoment(int degree){
		this.degree=degree;
	}
	
	public ZernikeMoment(int degree, RadialValue[] rv){
		this.degree = degree;
		this.rv = rv;
	}
	
	public double calculateRadial(double r, int m, int n, RadialValue rv){
		
		if(n<m || n<0 || m<0)
			return 0;
		
		//Check if radial value for m and n already present.
		if(rv!=null && rv.get(m, n)!=0)
			return rv.get(m, n);
		
		if (n==0 && m==0)
			return 1;
		
		if ( (n-m)%2==0 )
			return (r*(calculateRadial(r,abs(m-1),n-1,rv)+calculateRadial(r,m+1,n-1,rv))-calculateRadial(r,m,n-2,rv));	
		
		else
			return 0;
	}
	
	public void calculateRadius(ImageProcessor ip){
		centerX = ip.getWidth() / 2;
        centerY = ip.getHeight() / 2;
        final int max = max(centerX, centerY);
        radius = sqrt(2 * max * max);
	}

	public ComplexArray  extractZernikeMoment(ImageProcessor ip){
		//System.out.println("Start Zernike moment extraction process");
		calculateRadius(ip);
		
		ArrayList<Double> real = null; 
    	ArrayList<Double> imag = null;
    	if(rv==null)
    		rv = new RadialValue[ip.getHeight()*ip.getWidth()];
    
    	// TODO change into PixLib form
    	final int sz=ip.getHeight()*ip.getWidth();
    	Zps[] zps=new Zps[sz];
    	//ComplexArray[] zps2=  new ComplexArray[sz];
    	int index=0;
        for(int i=0;i<ip.getHeight();i++){
        	for(int j=0;j<ip.getWidth();j++){
        		final int x = j-centerX;
        		final int y = i-centerY;
        		final double r = Math.sqrt((x * x) + (y * y)) / radius;
        		//For each pixel create zps object
        		
        		zps[index]=new Zps();
        		
        		if(rv[index]==null)
        			rv[index] = new RadialValue(degree,degree);
        		
        		real=new ArrayList<>();
        		imag=new ArrayList<>();
        		
        		for(int k=0;k<=degree;k++){
        			for(int l=0;l<=k;l++){
        				
        				if((k-l)%2==0){
        					//Calculate radial_value
        					final double rr = calculateRadial(r, l, k, rv[index])* (degree + 1);
        					final double angle = l * Math.atan2(y, x);
        					final double pixel = ip.getPixel(x, y);
        	        		real.add(pixel * rr * cos(angle));
        	        		imag.add(pixel * rr * sin(angle));
        	        		rv[index].set(l, k, rr); 
        				}
        			}
        		}
        		
        		zps[index].setComplex(real, imag);
        		
        		index++;
        		
        		 	
         	}
       }
        
        double[] real_result=new double[real.size()];
        double[] imag_result=new double[real.size()];
        
        for(int i=0;i<zps.length;i++){
        	ArrayList<Double> temp=zps[i].getReal();
        	for(int j=0;j<temp.size();j++){
        		real_result[j]+=(temp.get(j)) / PI;
        	}
        	temp=zps[i].getImaginary();
        	for(int j=0;j<temp.size();j++){
        		imag_result[j]+=(temp.get(j)) / PI;
        	}
        }
        /*for(int i=0;i<real_result.length;i++){
        	System.out.println("Real Value:-" +real_result[i]+" Imaginary Value:- "+ imag_result[i]);
        }*/
        
		return new ComplexArray(real_result, imag_result, false);
	}
	
	
	public static void main(String[] args){
		//String path="/home/mg/Downloads/tifs/image.tif";
		IJ.run("Blobs (25K)");
    	//ImagePlus imp=IJ.openImage(path);
		ImagePlus imp=IJ.getImage();
    	//ImageConverter ic=new ImageConverter(imp);
    	//ic.convertToGray8();
    	
    	ImageProcessor ip=imp.getProcessor();
    	ZernikeMoment zm=new ZernikeMoment(8);
    	long aa=System.currentTimeMillis();
    	zm.extractZernikeMoment(ip);
    	long bb=System.currentTimeMillis();
    	System.out.println(bb-aa);
	}
	

}
