# Base de datos

# valores fijos, usados por índice

# Estados de asistencia

ESTADOS_ASISTENCIA = ["Presente", "Ausente justificado", "Ausente injustificado"]
EA_PRESENTE = 0; EA_AUS_J = 1; EA_AUS_I = 2

# Estados de alumno

ESTADOS_ALUMNO = ["Activo", "Inactivo"]
EAL_ACTIVO = 0; EAL_INACTIVO = 1

# bases iniciales

# Docentes: [legajo, dni, clave, Nombre, Apellido, mail]
DOCENTES = [
    [2001, "12345678", "Clave.123", "Carlos", "Gonzalez", "cgonzalez@uade.edu.ar"],
]
DO_LEGAJO = 0; DO_DNI = 1; DO_CLAVE = 2; DO_NOMBRE = 3; DO_APELLIDO = 4; DO_EMAIL = 5

# Clases: [Id, materia, fecha, día y horario]

CLASES = [
    [3001, "Matemática", "2025-08-05", "Martes", "14:00 - 18:00"],
    [3002, "Matemática", "2025-08-12", "Martes", "14:00 - 18:00"],
    [3003, "Matemática", "2025-08-19", "Martes", "14:00 - 18:00"],
    [3004, "Matemática", "2025-08-26", "Martes", "14:00 - 18:00"],
    [3005, "Matemática", "2025-09-02", "Martes", "14:00 - 18:00"],
    [3006, "Matemática", "2025-09-09", "Martes", "14:00 - 18:00"],
    [3007, "Matemática", "2025-09-16", "Martes", "14:00 - 18:00"],
    [3008, "Matemática", "2025-09-23", "Martes", "14:00 - 18:00"],
    [3009, "Matemática", "2025-09-30", "Martes", "14:00 - 18:00"],
    [3010, "Matemática", "2025-10-07", "Martes", "14:00 - 18:00"],
    [3011, "Matemática", "2025-10-14", "Martes", "14:00 - 18:00"],
    [3012, "Matemática", "2025-10-21", "Martes", "14:00 - 18:00"],
    [3013, "Matemática", "2025-10-28", "Martes", "14:00 - 18:00"],
    [3014, "Matemática", "2025-11-04", "Martes", "14:00 - 18:00"],
    [3015, "Matemática", "2025-11-11", "Martes", "14:00 - 18:00"],
    [3016, "Matemática", "2025-11-18", "Martes", "14:00 - 18:00"],
    [3017, "Matemática", "2025-11-25", "Martes", "14:00 - 18:00"],
]
CL_ID = 0; CL_MATERIA = 1; CL_FECHA = 2; CL_DIA = 3; CL_HORARIO = 4

# Variable de trabajo alumnos

# alumnos: [legajo, dni, apellido, nombre, fecha_nac, email, estado_alumno_idx]

alumnos = [
    [1001, "40111222", "Saltid", "Juan", "08-09-2007", "jsaltid@uade.edu.ar", EAL_ACTIVO],
    [1002, "39222333", "Altanio", "Pablo", "19-04-2004", "paltanio@uade.edu.ar", EAL_ACTIVO],
    [1003, "45444555", "Mandeo", "Marcelo", "02-12-2007", "mmandeo@uade.edu.ar", EAL_ACTIVO],
    [1004, "42111666", "Fernandez", "Mateo", "16-03-2005", "mfernandez@uade.edu.ar", EAL_ACTIVO],
    [1005, "43777888", "Castro", "Lucia", "17-07-2006", "lucastro@uade.edu.ar", EAL_ACTIVO],
    [1006, "38999111", "Martinez", "Julian", "06-05-2003", "jmartinez@uade.edu.ar", EAL_ACTIVO],
    [1007, "40222444", "Nando", "Sofia", "13-07-2004", "snando@uade.edu.ar", EAL_ACTIVO],
    [1008, "45555666", "Gonzales", "Agustina", "09-03-2007", "agonzales@uade.edu.ar", EAL_ACTIVO],
    [1009, "47777888", "Ameglio", "Franchesca", "11-09-2006", "fameglio@uade.edu.ar", EAL_ACTIVO],
    [1010, "42223333", "Ayala", "Joaquin", "20-08-2007", "jayala@uade.edu.ar", EAL_ACTIVO],
    [1011, "43333444", "Catillo", "Valentina", "01-02-2005", "vcastillo@uade.edu.ar", EAL_ACTIVO],
    [1012, "45555777", "Nuñez", "Lautaro", "18-04-2006", "lnuñez@uade.edu.ar", EAL_ACTIVO],
    [1013, "46666888", "Espinosa", "Florencia", "30-01-2007", "fespinosa@uade.edu.ar", EAL_ACTIVO],
    [1014, "48888999", "Fuentes", "Tomas", "23-03-2004", "tfuentes@uade.edu.ar", EAL_ACTIVO],
    [1015, "47788999", "Flores", "Faustina", "12-08-2006", "fflores@uade.edu.ar", EAL_ACTIVO],
]
AL_LEGAJO = 0; AL_DNI = 1; AL_APELLIDO = 2; AL_NOMBRE = 3; AL_FECHA_NAC = 4; AL_EMAIL = 5; AL_ESTADO_IDX = 6

# Transacciones con matriz presentismo

# Cada fila de presentismo: [materia_idx, clase_idx, alumno_legajo, estado_asistencia_idx, estado_alumno_idx]

PR_CLASE_IDX = 1; PR_ALUMNO_LEGAJO = 2; PR_ESTADO_ASIST_IDX = 3; PR_ESTADO_ALUMNO_IDX = 4