package test;

import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class AnnotationIntrospector {

   
    public static Annotation[] getClassAnnotations(Class<?> clazz) {
        return clazz.getAnnotations();
    }

    public static Annotation[] getMethodAnnotations(Class<?> clazz, String methodName) {

        Annotation[] annotations = null;
        try {
            Class<?>[] params = null;
            Method method = clazz.getDeclaredMethod(methodName, params);
            if (method != null) {
                annotations = method.getAnnotations();
            }
        } catch (SecurityException e) {
            e.printStackTrace();
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        }
        return annotations;
    }

    public static Annotation[] getFieldAnnotations(Class<?> clazz, String fieldName) throws NoSuchFieldException{
        Annotation[] annotations = null;
        try {
            Field field = clazz.getDeclaredField(fieldName);
            if (field != null) {
            	//System.out.println("nn");
                annotations = field.getAnnotations();
            }
        } catch (SecurityException e) {
            e.printStackTrace();
        }
        return annotations;
    }

   
    public static void printAnnotations(Annotation[] ann) {
        if (ann == null)
            return;
        for (Annotation a : ann) {
            System.out.println(a.toString());
        }
    }
}