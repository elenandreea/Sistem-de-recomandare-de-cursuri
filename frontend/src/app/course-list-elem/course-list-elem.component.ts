import { Component, OnInit } from '@angular/core';
import { Input } from '@angular/core';
import { Course } from '../course';

@Component({
  selector: 'app-course-list-elem',
  templateUrl: './course-list-elem.component.html',
  styleUrls: ['./course-list-elem.component.css']
})
export class CourseListElemComponent implements OnInit {

  @Input('course') course: Course;
  
  showUdemy: boolean;
  route: string;

  constructor() {}
  
  ngOnInit(): void {
    if(this.course.website == "Udemy") {
      this.showUdemy = true;
    }
    if(this.course.difficulty == "None") {
      this.course.difficulty = "All Levels";
    }
    this.route= "/course/"+this.course.id;
  }

}
