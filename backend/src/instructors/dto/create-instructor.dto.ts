export class CreateInstructorDto {
  instructor_fname: string;
  instructor_mname: string;
  instructor_lname: string;
  instructor_gender: string;
  instructor_jobtype: string;
  institute_id?: number;
  program_id?: number;
  instructor_expertise?: string[]; // Add this if not already present
}
